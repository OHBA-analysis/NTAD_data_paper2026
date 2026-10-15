#!/usr/bin/env python3
"""
Scanner-change validation figure for NTAD MEG dataset (Nature Data paper).

Cambridge replaced its Elekta Vectorview ("old") with a MEGIN Triux Neo
("new") partway through NTAD. Five healthy volunteers were scanned twice on
each system (old_1, old_2, new_1, new_2) with the full NTAD protocol. The
question is whether the scanner change adds variability beyond ordinary
session-to-session (test-retest) variability.

Approach (sensor-level "fingerprinting"):
  * per recording, per-channel features: resting log-PSD (1-40 Hz) and task
    evoked responses (0.5-30 Hz, signed, post-stimulus window);
  * Pearson similarity between every pair of the 20 recordings, using only
    channels that are good in both;
  * pairs grouped as same/different subject × same/different scanner.
If the scanner change is benign, same-subject similarity across scanners
should match same-subject similarity within a scanner, and both should far
exceed between-subject similarity.

Figures (gradiometers main, magnetometers supplementary):
  a  per-subject eyes-closed PSDs, four sessions overlaid
  b  20 × 20 recording similarity matrix (eyes closed)
  c  similarity by comparison type for all six measures, one point per subject

Per-recording features are cached so plotting can be re-run independently.
"""

import os
import csv
import pickle
import numpy as np
from glob import glob
from itertools import combinations
from joblib import Parallel, delayed
import mne
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

# ── paths ─────────────────────────────────────────────────────────────────────
BASE  = '/ohba/pi/mwoolrich/raw_datasets/ntad/cambridge/scanner_validation'
OUT   = '/ohba/pi/mwoolrich/datasets/ntad/preprocessed/technical_validation/scanner_validation'
CACHE = f'{OUT}/cache'
os.makedirs(CACHE, exist_ok=True)

# val05 has no new-scanner sessions and is excluded.
SUBJECTS = ['val01', 'val02', 'val03', 'val04', 'val06']
SESSIONS = ['old_1', 'old_2', 'new_1', 'new_2']
SES_LABEL = {'old_1': 'O1', 'old_2': 'O2', 'new_1': 'N1', 'new_2': 'N2'}
RECS = [(s, ses) for s in SUBJECTS for ses in SESSIONS]   # fixed row order

N_JOBS = 12
CENTRE_FEATURES = True   # subtract the across-recording mean before correlating
CH_TYPES = ('grad', 'mag')
SCALE = {'grad': 1e26, 'mag': 1e30}   # → (fT/cm)²/Hz, fT²/Hz
UNIT  = {'grad': '(fT/cm)²/Hz', 'mag': 'fT²/Hz'}
GFP_SCALE = {'grad': 1e13, 'mag': 1e15}   # T/m → fT/cm, T → fT
GFP_UNIT  = {'grad': 'fT/cm', 'mag': 'fT'}

# Events on STI101: site-sync pulses use bits 8 (=256, Oxford) and 12 (=4096,
# Cambridge) and are masked out, as in 04_technical_validation.py.
MASK = 4352
# On the Triux Neo one trigger bit chatters on/off at ~2-6 ms intervals during
# each ~20-50 ms pulse (e.g. 22↔30, 33↔35), so a plain find_events assigns the
# wrong code to ~half the triggers. A bit belongs to the code if it is high for
# at least this fraction of the pulse.
BIT_ON_FRAC = 0.75

# Trigger→stimulus delays (ms) per scanner, from MEG_metadata.csv
# (visual_delay / auditory_delay; majority value per Cambridge scanner). The
# visual delay differs by 15 ms between setups, which is confirmed by the
# uncorrected old-vs-new evoked latency shift. Evoked responses are shifted
# earlier by this amount so they are aligned to stimulus onset.
DELAYS_MS = {'old': {'visual': 35, 'auditory': 26},
             'new': {'visual': 20, 'auditory': 26}}
_DELAY_PAD_S = 0.1   # extra epoch length so the shift never extrapolates

# Task definitions mirror 04_technical_validation.py.
MEASURES = [
    # key, folder, short label, kind, spec
    ('rsc', 6, 'Rest EC', 'psd', None),
    ('rso', 5, 'Rest EO', 'psd', None),
    ('t1',  1, 'AV',      'evoked',
     dict(event_id={'Auditory': 22, 'Visual': 33}, tmin=-0.2, tmax=0.5,
          modality={'Auditory': 'auditory', 'Visual': 'visual'})),
    ('t2',  2, 'MMN',     'evoked',
     dict(event_id={'Deviant': 100, 'Standard': 101}, tmin=-0.2, tmax=0.5,
          recode={101: list(range(101, 111))},
          modality={'Deviant': 'auditory', 'Standard': 'auditory'})),
    ('t3',  3, 'Scene',   'evoked',
     dict(event_id={'Novel': 22, 'Familiar': 33}, tmin=-0.2, tmax=0.7,
          modality={'Novel': 'visual', 'Familiar': 'visual'})),
    ('t4',  4, 'VAO',     'evoked',
     dict(event_id={'Standard': 10, 'Aud. deviant': 20, 'Novel deviant': 30},
          tmin=-0.2, tmax=0.8,
          # epochs are anchored to the visual trigger
          modality={'Standard': 'visual', 'Aud. deviant': 'visual',
                    'Novel deviant': 'visual'})),
]
MEASURE_BY_KEY = {m[0]: m for m in MEASURES}


def rec_file(sub, ses, folder):
    hits = glob(f'{BASE}/{sub}/{sub}_{ses}/{folder}/preprocessed/*_preproc_raw.fif')
    return hits[0] if len(hits) == 1 else None


# ── per-recording feature extraction ──────────────────────────────────────────

def robust_events(raw):
    """Decode STI101 pulse-by-pulse, keeping only bits high for most of the pulse."""
    sti = raw.get_data(picks='STI101')[0].astype(np.int64) & ~MASK
    edges = np.diff(np.r_[0, (sti > 0).astype(int), 0])
    starts, stops = np.flatnonzero(edges == 1), np.flatnonzero(edges == -1)
    events = []
    for a, b in zip(starts, stops):
        seg = sti[a:b]
        code = sum(1 << k for k in range(16)
                   if ((seg >> k) & 1).mean() >= BIT_ON_FRAC)
        if code:
            events.append([a + raw.first_samp, 0, code])
    return np.array(events, dtype=int).reshape(-1, 3)


def _meg_layout(info):
    """Return {ch_type: (names, bad_mask)} including bad channels."""
    out = {}
    for ct in CH_TYPES:
        picks = mne.pick_types(info, meg=ct, exclude=[])
        names = [info['ch_names'][p] for p in picks]
        out[ct] = (names, np.array([n in info['bads'] for n in names]))
    return out


def psd_features(fif, fmin=1.0, fmax=40.0):
    raw = mne.io.read_raw_fif(fif, preload=True, verbose=False)
    n_per_seg = int(4 * raw.info['sfreq'])
    out = dict(head_pos=raw.info['dev_head_t']['trans'][:3, 3] * 1000)
    layout = _meg_layout(raw.info)
    raw.info['bads'] = []   # compute_psd drops bads even when named; mask kept in layout
    for ct, (names, bad) in layout.items():
        psd = raw.compute_psd(method='welch', fmin=fmin, fmax=fmax,
                              n_fft=n_per_seg, n_per_seg=n_per_seg,
                              picks=names, verbose=False)
        data, freqs = psd.get_data(return_freqs=True)
        data = data * SCALE[ct]
        out[ct] = dict(names=names, bad=bad, freqs=freqs,
                       chan_db=10 * np.log10(np.maximum(data, 1e-30)),
                       # sensor-mean over good channels, as in 04 (mean, then dB)
                       mean_db=10 * np.log10(data[~bad].mean(axis=0)))
    return out


def _shift(data, times, delay_s):
    """Shift responses earlier by delay_s on the same time axis (as in 04)."""
    return np.array([np.interp(times + delay_s, times, ch) for ch in data])


def evoked_features(fif, event_id, tmin, tmax, scanner, modality,
                    recode=None):
    raw = mne.io.read_raw_fif(fif, preload=True, verbose=False)
    events = robust_events(raw)
    raw.filter(0.5, 30.0, picks='meg', verbose=False)
    if recode:
        for new_code, old_codes in recode.items():
            events[np.isin(events[:, 2], old_codes), 2] = new_code
    present = {c: v for c, v in event_id.items() if (events[:, 2] == v).any()}
    epochs = mne.Epochs(raw, events, event_id=present, tmin=tmin,
                        tmax=tmax + _DELAY_PAD_S,
                        baseline=(None, 0), picks=mne.pick_types(raw.info, meg=True, exclude=[]),
                        preload=True, reject_by_annotation=True, verbose=False)
    out = dict(head_pos=raw.info['dev_head_t']['trans'][:3, 3] * 1000,
               n_trials={c: len(epochs[c]) for c in present})
    for ct, (names, bad) in _meg_layout(raw.info).items():
        keep = epochs.times <= tmax + 1e-9
        conds = {c: _shift(epochs[c].average(picks=names).data, epochs.times,
                           DELAYS_MS[scanner][modality[c]] / 1000)[:, keep]
                 for c in present}
        out[ct] = dict(names=names, bad=bad, times=epochs.times[keep],
                       conds=conds)
    return out


def _cache_path(key, sub, ses):
    return f'{CACHE}/{key}_{sub}_{ses}.pkl'


def _compute_one(key, sub, ses, overwrite):
    pth = _cache_path(key, sub, ses)
    if not overwrite and os.path.exists(pth):
        return
    _, folder, _, kind, spec = MEASURE_BY_KEY[key]
    fif = rec_file(sub, ses, folder)
    if fif is None:
        print(f'  missing: {sub} {ses} {key}')
        return
    try:
        feat = (psd_features(fif) if kind == 'psd' else
                evoked_features(fif, scanner=ses.split('_')[0], **spec))
    except Exception as e:
        print(f'  skip {sub} {ses} {key}: {type(e).__name__}: {e}')
        return
    with open(pth, 'wb') as fh:
        pickle.dump(feat, fh)


def compute_all(overwrite=False):
    jobs = [(m[0], sub, ses) for m in MEASURES for sub, ses in RECS]
    Parallel(n_jobs=N_JOBS, verbose=5)(
        delayed(_compute_one)(k, s, ses, overwrite) for k, s, ses in jobs)


def load_features(key):
    """Return list (aligned with RECS) of feature dicts or None."""
    feats = []
    for sub, ses in RECS:
        pth = _cache_path(key, sub, ses)
        if os.path.exists(pth):
            with open(pth, 'rb') as fh:
                feats.append(pickle.load(fh))
        else:
            feats.append(None)
    return feats


# ── similarity ────────────────────────────────────────────────────────────────

def feature_matrix(feats, ct, kind):
    """Stack per-recording features into (n_recs, n_channels, n_features).

    Channels are aligned by name (channel order differs between systems);
    bad channels are NaN. Evoked features are the signed post-stimulus
    responses of all conditions, concatenated.
    """
    ref = next(f for f in feats if f is not None)[ct]
    names = sorted(ref['names'])
    rows = []
    for f in feats:
        if f is None:
            rows.append(None)
            continue
        d = f[ct]
        idx = [d['names'].index(n) for n in names]
        if kind == 'psd':
            x = d['chan_db'][idx]
        else:
            post = d['times'] >= 0
            x = np.concatenate([d['conds'][c][idx][:, post] * GFP_SCALE[ct]
                                for c in sorted(d['conds'])], axis=1)
        x = x.astype(float)
        x[d['bad'][idx]] = np.nan
        rows.append(x)
    shape = next(r for r in rows if r is not None).shape
    X = np.full((len(rows),) + shape, np.nan)
    for i, r in enumerate(rows):
        if r is not None and r.shape == shape:
            X[i] = r
        elif r is not None:
            print(f'  shape mismatch for {RECS[i]} ({r.shape} vs {shape}); dropped')
    return X


def similarity_matrix(X):
    """Pearson r between every pair of recordings over channels good in both."""
    if CENTRE_FEATURES:
        X = X - np.nanmean(X, axis=0, keepdims=True)
    n = len(X)
    S = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(n):
            a, b = X[i], X[j]
            ok = ~np.isnan(a[:, 0]) & ~np.isnan(b[:, 0])
            if ok.sum() < 10:
                continue
            S[i, j] = np.corrcoef(a[ok].ravel(), b[ok].ravel())[0, 1]
    return S


CATEGORIES = [
    ('ss_same', 'Same subject\nsame scanner'),
    ('ss_cross', 'Same subject\nacross scanners'),
    ('ds_same', 'Different subjects\nsame scanner'),
    ('ds_cross', 'Different subjects\nacross scanners'),
]


def _pair_category(i, j):
    (si, ei), (sj, ej) = RECS[i], RECS[j]
    same_sub = si == sj
    same_scn = ei.split('_')[0] == ej.split('_')[0]
    return ('ss_' if same_sub else 'ds_') + ('same' if same_scn else 'cross')


def summarise(S):
    """Per-subject mean similarity per category (one value per subject), and
    cross-scanner identification accuracy (each recording matched to its most
    similar recording on the other scanner)."""
    per_sub = {c: {s: [] for s in SUBJECTS} for c, _ in CATEGORIES}
    for i, j in combinations(range(len(RECS)), 2):
        if np.isnan(S[i, j]):
            continue
        cat = _pair_category(i, j)
        per_sub[cat][RECS[i][0]].append(S[i, j])
        if RECS[j][0] != RECS[i][0]:
            per_sub[cat][RECS[j][0]].append(S[i, j])
    per_sub = {c: np.array([np.mean(v[s]) if v[s] else np.nan for s in SUBJECTS])
               for c, v in per_sub.items()}

    hits = n = 0
    for i, (sub, ses) in enumerate(RECS):
        other = [j for j, (_, e) in enumerate(RECS)
                 if e.split('_')[0] != ses.split('_')[0] and not np.isnan(S[i, j])]
        if not other:
            continue
        best = other[int(np.argmax(S[i, other]))]
        hits += RECS[best][0] == sub
        n += 1
    return per_sub, (hits, n)


# ── diagnostics ───────────────────────────────────────────────────────────────

def gfp_curve(d, ct):
    """GFP of the condition-averaged evoked response (good channels only)."""
    evo = np.mean([d[ct]['conds'][c] for c in d[ct]['conds']], axis=0)
    evo = evo[~d[ct]['bad']] * GFP_SCALE[ct]
    g = np.sqrt((evo ** 2).mean(axis=0))
    return g - g[d[ct]['times'] < 0].mean()


def evoked_lag_ms(feats, ct, max_lag_ms=60):
    """Per subject: lag (ms) maximising the cross-correlation of old- vs
    new-scanner mean GFP. Positive = new-scanner response later."""
    lags = {}
    for sub in SUBJECTS:
        g = {scn: [gfp_curve(f, ct) for f, (s, e) in zip(feats, RECS)
                   if f is not None and s == sub and e.startswith(scn)]
             for scn in ('old', 'new')}
        if not g['old'] or not g['new']:
            continue
        a, b = np.mean(g['old'], axis=0), np.mean(g['new'], axis=0)
        times = next(f for f in feats if f is not None)[ct]['times']
        post = times >= 0
        a, b = a[post] - a[post].mean(), b[post] - b[post].mean()
        sfreq = 1 / (times[1] - times[0])
        max_lag = int(max_lag_ms / 1000 * sfreq)
        xc = [np.dot(a[max(0, -k):len(a) - max(0, k)], b[max(0, k):len(b) - max(0, -k)])
              for k in range(-max_lag, max_lag + 1)]
        lags[sub] = (np.argmax(xc) - max_lag) / sfreq * 1000
    return lags


def write_diagnostics(all_feats):
    rows = []
    for key, *_ in MEASURES:
        for f, (sub, ses) in zip(all_feats[key], RECS):
            if f is None:
                rows.append([key, sub, ses, '', '', '', ''])
                continue
            hp = f['head_pos']
            ntr = f.get('n_trials', {})
            rows.append([key, sub, ses, *np.round(hp, 1),
                         ';'.join(f'{c}={n}' for c, n in ntr.items())])
    path = f'{OUT}/recording_diagnostics.csv'
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['measure', 'subject', 'session', 'head_x_mm', 'head_y_mm',
                    'head_z_mm', 'n_trials'])
        w.writerows(rows)
    print(f'Saved → {path}')

    hp = np.array([[float(r[3]), float(r[4]), float(r[5])] for r in rows if r[3] != ''])
    scn = np.array([r[2].split('_')[0] for r in rows if r[3] != ''])
    for s in ('old', 'new'):
        m, sd = hp[scn == s].mean(axis=0), hp[scn == s].std(axis=0)
        print(f'  head position {s}: x={m[0]:.1f}±{sd[0]:.1f}  y={m[1]:.1f}±{sd[1]:.1f}  '
              f'z={m[2]:.1f}±{sd[2]:.1f} mm (device frame)')

    print('  residual old→new evoked latency shift after delay correction '
          '(grad GFP xcorr, ms, + = new later):')
    for key, _, label, kind, _ in MEASURES:
        if kind != 'evoked':
            continue
        lags = evoked_lag_ms(all_feats[key], 'grad')
        print(f'    {label:6s} ' + '  '.join(f'{s}:{v:+.0f}' for s, v in lags.items()))


# ── plotting ──────────────────────────────────────────────────────────────────
# Scanner identity: blue = Vectorview (old), orange = Triux Neo (new); session
# 1/2 by line style. Comparison type: aqua = same subject, grey = different
# subjects; filled = same scanner, open = across scanners.

C_OLD, C_NEW = '#2a78d6', '#eb6834'
C_SAME, C_DIFF = '#1baf7a', '#8a8984'
INK, INK_2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
SES_STYLE = {'old_1': (C_OLD, '-'), 'old_2': (C_OLD, '--'),
             'new_1': (C_NEW, '-'), 'new_2': (C_NEW, '--')}
CAT_STYLE = {'ss_same': (C_SAME, True), 'ss_cross': (C_SAME, False),
             'ds_same': (C_DIFF, True), 'ds_cross': (C_DIFF, False)}

plt.rcParams.update({
    'font.size': 8, 'axes.titlesize': 9, 'axes.labelsize': 8,
    'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 7,
    'axes.edgecolor': INK_2, 'axes.labelcolor': INK, 'xtick.color': INK_2,
    'ytick.color': INK_2, 'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 0.6, 'pdf.fonttype': 42,
})


def _panel_label(ax, s, x=-0.12, y=1.06):
    ax.text(x, y, s, transform=ax.transAxes, fontsize=12, fontweight='bold',
            va='bottom', ha='right', color=INK)


def plot_subject_curves(axes, feats, ct, kind, ylabel, show_legend):
    """One small panel per subject with the four sessions overlaid."""
    for k, (ax, sub) in enumerate(zip(axes, SUBJECTS)):
        for f, (s, ses) in zip(feats, RECS):
            if s != sub or f is None:
                continue
            col, ls = SES_STYLE[ses]
            if kind == 'psd':
                x, y = f[ct]['freqs'], f[ct]['mean_db']
            else:
                x, y = f[ct]['times'] * 1000, gfp_curve(f, ct)
            ax.plot(x, y, color=col, ls=ls, lw=1.1, label=SES_LABEL[ses])
        if kind == 'psd':
            ax.axvspan(7, 13, color=GRID, alpha=0.6, lw=0, zorder=0)
            ax.set_xlim(1, 40)
            ax.set_xticks([1, 10, 20, 30, 40])
        else:
            ax.axvline(0, color=INK_2, lw=0.6, ls=':')
            ax.set_xlim(x[0], x[-1])
        ax.set_title(sub, color=INK)
        if k == 0:
            ax.set_ylabel(ylabel)
        else:
            ax.tick_params(labelleft=False)
        if show_legend and k == len(SUBJECTS) - 1:
            ax.legend(frameon=False, loc='upper right', handlelength=1.8,
                      title='Session', title_fontsize=7)


def plot_matrix(ax, S):
    """Diverging scale centred on 0 (features are mean-centred); the trivial
    diagonal (r = 1) is blanked so it does not set the colour range."""
    n = len(RECS)
    S = S.copy()
    S[np.eye(n, dtype=bool)] = np.nan
    vmax = np.ceil(np.nanmax(np.abs(S)) * 10) / 10
    cmap = plt.get_cmap('RdGy_r').copy()
    cmap.set_bad('white')
    im = ax.imshow(S, cmap=cmap, vmin=-vmax, vmax=vmax,
                   interpolation='nearest')
    for k in range(1, len(SUBJECTS)):
        ax.axhline(4 * k - 0.5, color='white', lw=1.6)
        ax.axvline(4 * k - 0.5, color='white', lw=1.6)
    # dotted old/new split inside each subject's block
    for k in range(len(SUBJECTS)):
        a, b = 4 * k - 0.5, 4 * k + 3.5
        ax.plot([a, b], [4 * k + 1.5] * 2, color=INK_2, lw=0.6, ls=':')
        ax.plot([4 * k + 1.5] * 2, [a, b], color=INK_2, lw=0.6, ls=':')
    centres = [4 * k + 1.5 for k in range(len(SUBJECTS))]
    ax.set_xticks(centres)
    ax.set_xticklabels(SUBJECTS, rotation=0)
    ax.set_yticks(centres)
    ax.set_yticklabels(SUBJECTS)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    cax = ax.inset_axes([1.04, 0, 0.04, 1])
    cb = plt.colorbar(im, cax=cax)
    cb.set_label('Similarity (r)')
    cb.outline.set_visible(False)
    ax.set_title('Recording × recording similarity, eyes closed\n'
                 '(within blocks: O1, O2 | N1, N2)', color=INK)


def plot_strip(ax, summaries):
    """x groups = measures; within each, the four comparison types."""
    offs = np.array([-0.27, -0.09, 0.09, 0.27])
    rng = np.random.default_rng(0)
    for g, (key, label, (per_sub, (hits, n))) in enumerate(summaries):
        for (cat, _), dx in zip(CATEGORIES, offs):
            col, filled = CAT_STYLE[cat]
            y = per_sub[cat]
            x = g + dx + rng.uniform(-0.025, 0.025, len(y))
            ax.scatter(x, y, s=16, facecolor=col if filled else 'white',
                       edgecolor=col, linewidth=1.0, zorder=3)
            ax.plot([g + dx - 0.06, g + dx + 0.06], [np.nanmean(y)] * 2,
                    color=INK, lw=1.2, zorder=4)
        # pair each subject's within- and across-scanner same-subject values
        for a, b in zip(per_sub['ss_same'], per_sub['ss_cross']):
            ax.plot([g + offs[0], g + offs[1]], [a, b], color=C_SAME,
                    lw=0.5, alpha=0.5, zorder=2)
        ax.text(g, 1.02, f'ID {hits}/{n}', transform=ax.get_xaxis_transform(),
                ha='center', va='bottom', fontsize=7, color=INK_2)
    ax.set_xticks(range(len(summaries)))
    ax.set_xticklabels([s[1] for s in summaries])
    ax.set_xlim(-0.5, len(summaries) - 0.5)
    ax.axhline(0, color=INK_2, lw=0.6)
    ax.set_ylabel('Similarity (r), mean per subject')
    ax.yaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    handles = [Line2D([], [], ls='', marker='o', markersize=5,
                      markerfacecolor=CAT_STYLE[c][0] if CAT_STYLE[c][1] else 'white',
                      markeredgecolor=CAT_STYLE[c][0], label=lab.replace('\n', ' '))
               for c, lab in CATEGORIES]
    ax.legend(handles=handles, frameon=False, ncol=2, loc='upper center',
              bbox_to_anchor=(0.5, -0.1))
    ax.set_title('Similarity by comparison type, all measures', color=INK, pad=14)


def plot_main(all_feats, sims, summaries, ct, tag):
    fig = plt.figure(figsize=(11, 7.6))
    outer = gridspec.GridSpec(2, 1, figure=fig, height_ratios=[1, 1.55],
                              hspace=0.42)
    top = gridspec.GridSpecFromSubplotSpec(1, 5, outer[0], wspace=0.08)
    axes_a = [fig.add_subplot(top[0, k]) for k in range(5)]
    for ax in axes_a[1:]:
        ax.sharey(axes_a[0])
    plot_subject_curves(axes_a, all_feats['rsc'], ct, 'psd',
                        f'Power (dB re. {UNIT[ct]})', show_legend=True)
    fig.text(0.5, axes_a[0].get_position().y0 - 0.055, 'Frequency (Hz)',
             ha='center', fontsize=8, color=INK)
    _panel_label(axes_a[0], 'a', x=-0.28)

    bottom = gridspec.GridSpecFromSubplotSpec(1, 2, outer[1], wspace=0.4,
                                              width_ratios=[1.0, 1.75])
    ax_b = fig.add_subplot(bottom[0, 0])
    plot_matrix(ax_b, sims['rsc'])
    _panel_label(ax_b, 'b', x=-0.14)

    ax_c = fig.add_subplot(bottom[0, 1])
    plot_strip(ax_c, summaries)
    _panel_label(ax_c, 'c', x=-0.08)

    for fmt in ('png', 'pdf'):
        path = f'{OUT}/scanner_validation{tag}.{fmt}'
        fig.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0.05)
        print(f'Saved → {path}')
    plt.close(fig)


def plot_overlays_supp(all_feats, ct, tag):
    """All measures except eyes-closed (shown in the main figure), per subject."""
    rows = [m for m in MEASURES if m[0] != 'rsc']
    fig, axes = plt.subplots(len(rows), 5, figsize=(11, 2.0 * len(rows)),
                             sharex='row', sharey='row')
    for r, (key, _, label, kind, _) in enumerate(rows):
        ylabel = (f'{label}\nPower (dB)' if kind == 'psd'
                  else f'{label}\nGFP ({GFP_UNIT[ct]})')
        plot_subject_curves(axes[r], all_feats[key], ct, kind, ylabel,
                            show_legend=(r == 0))
        if r > 0:
            for ax in axes[r]:
                ax.set_title('')
        xl = 'Frequency (Hz)' if kind == 'psd' else 'Time (ms)'
        axes[r, 2].set_xlabel(xl)
    fig.tight_layout(h_pad=1.2)
    for fmt in ('png', 'pdf'):
        path = f'{OUT}/scanner_validation_overlays{tag}.{fmt}'
        fig.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0.05)
        print(f'Saved → {path}')
    plt.close(fig)


def write_summary(results):
    path = f'{OUT}/similarity_summary.csv'
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['ch_type', 'measure', 'category', *SUBJECTS, 'mean',
                    'cross_scanner_id_hits', 'cross_scanner_id_n'])
        for ct, summaries in results.items():
            for key, label, (per_sub, (hits, n)) in summaries:
                for cat, _ in CATEGORIES:
                    v = per_sub[cat]
                    w.writerow([ct, label, cat, *np.round(v, 3),
                                round(float(np.nanmean(v)), 3), hits, n])
    print(f'Saved → {path}')
    for ct, summaries in results.items():
        print(f'  {ct}: mean similarity  ss_same / ss_cross / ds_same / ds_cross  (cross-scanner ID)')
        for key, label, (per_sub, (hits, n)) in summaries:
            m = [np.nanmean(per_sub[c]) for c, _ in CATEGORIES]
            print(f'    {label:8s} ' + ' / '.join(f'{x:.2f}' for x in m) + f'   ({hits}/{n})')


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='NTAD Cambridge scanner-change validation')
    p.add_argument('--overwrite', action='store_true',
                   help='recompute cached per-recording features')
    args = p.parse_args()

    compute_all(overwrite=args.overwrite)
    all_feats = {m[0]: load_features(m[0]) for m in MEASURES}
    write_diagnostics(all_feats)

    results = {}
    for ct in CH_TYPES:
        sims, summaries = {}, []
        for key, _, label, kind, _ in MEASURES:
            sims[key] = similarity_matrix(feature_matrix(all_feats[key], ct, kind))
            summaries.append((key, label, summarise(sims[key])))
        results[ct] = summaries
        tag = '' if ct == 'grad' else '_mag'
        plot_main(all_feats, sims, summaries, ct, tag)
        plot_overlays_supp(all_feats, ct, tag)
    write_summary(results)
