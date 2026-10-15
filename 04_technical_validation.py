#!/usr/bin/env python3
"""
Technical validation figure for NTAD MEG dataset (Nature Data paper).

Four tasks (evoked responses) + resting state (power spectra).
Results are cached to a pickle so plotting can be re-run independently.
"""

import os
import re
import csv
import pickle
import numpy as np
from glob import glob
from joblib import Parallel, delayed
import mne
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import pandas as pd

# ── paths ─────────────────────────────────────────────────────────────────────
BASE = '/ohba/pi/mwoolrich/datasets/ntad/preprocessed'
OUT  = f'{BASE}/technical_validation'
os.makedirs(OUT, exist_ok=True)

# Events on STI101: site-sync pulses use bits 8 (=256, Oxford) and 12 (=4096,
# Cambridge). mask_type='not_and' keeps only events that have NEITHER bit set.
MASK      = 4352   # 256 | 4096
MASK_TYPE = 'not_and'
N_JOBS    = 12
PSD_STANDARDISE = False
PSD_AX = 1.0  # sqrt(f) axis for PSD plot (1.0 = linear, 0.5 = sqrt, 2.0 = f²)

# ── per-subject helpers ───────────────────────────────────────────────────────
df=pd.read_csv('/ohba/pi/mwoolrich/datasets/ntad/DataPortalIngest_March2025/ParticipantOverview.csv')
ntad_ids = list(df[df['analyseable_using_NTAD_criteria']=='Yes']['NTAD_ID'].unique())

# Site/scanner are NOT derivable from the ID prefix (C/P encode
# Control/Patient group, not acquisition site).
_meta_df = pd.read_csv(
    '/ohba/pi/mwoolrich/datasets/ntad/DataPortalIngest_March2025/MEG_metadata.csv',
    encoding='latin1')

# Scanner per recording, keyed by (NTAD_ID, visit code in the filename).
# Cambridge replaced its Elekta Neuromag (Vectorview) with an Elekta Triux Neo
# in Aug 2020, so a subject's site does not determine the scanner.
_VISIT_CODE = {'Baseline': 'bl', 'Baseline2': 'bl2', 'Two-week': 'tw',
               'Annual follow-up': 'af', 'Annual': 'af',
               'Annual follow-up2': 'af2'}
SCANNER_MAP = {(r.NTAD_ID, _VISIT_CODE[r.VISIT_ID]): r.SCANNER
               for r in _meta_df.itertuples()}

# Trigger→stimulus delays (s), measured in trigger_delay_measurements/: the
# STI101 trigger fires this much *before* the stimulus actually appears, so
# evoked responses must be shifted earlier by this amount to be correctly
# zero-aligned on stimulus onset rather than trigger onset.
# The Cambridge measurements date from May 2021, i.e. the Triux Neo. The
# Vectorview-era visual delay was longer: MEG_metadata.csv lists 35 vs 20 ms
# visual (26 vs 26 ms auditory) for the old vs new Cambridge setups, and the
# scanner-change validation data (05_scanner_validation.py) show the same
# ~15-20 ms earlier visual responses on the new system. Vectorview delays are
# therefore the measured Triux Neo delays plus that metadata offset.
_CAM_OLD_MINUS_NEW = {'auditory': 0.026 - 0.026, 'visual': 0.035 - 0.020}
DELAYS_S = {
    ('MEGIN TriuxNeo',   'auditory'): 0.0685,   # Oxford
    ('MEGIN TriuxNeo',   'visual'):   0.0100,
    ('Elekta Triux Neo', 'auditory'): 0.0670,   # Cambridge, from Aug 2020
    ('Elekta Triux Neo', 'visual'):   0.0120,
    ('Elekta Neuromag',  'auditory'): 0.0670 + _CAM_OLD_MINUS_NEW['auditory'],
    ('Elekta Neuromag',  'visual'):   0.0120 + _CAM_OLD_MINUS_NEW['visual'],
}

# On the Cambridge Triux Neo one trigger bit chatters on/off every ~2-6 ms
# within each ~20-50 ms pulse (22↔30, 33↔35, 44↔60, ...), so find_events
# assigns the wrong code to about half of the triggers. Triggers are therefore
# decoded pulse by pulse: a bit belongs to the code if it is high for at least
# this fraction of the pulse.
BIT_ON_FRAC = 0.75
# Extra tmax padding requested during epoching so the shift below (a forward
# resample) never has to extrapolate past the end of the epoched data.
_DELAY_PAD_S = 0.1


def _decode_sti(raw):
    """Decode STI101 pulse by pulse, robust to chattering trigger bits.

    Equivalent to find_events(mask=MASK, mask_type=MASK_TYPE, uint_cast=True)
    on clean recordings; see BIT_ON_FRAC for why it is needed.
    """
    sti = raw.get_data(picks='STI101')[0]
    sti = sti.astype(np.int64).astype(np.uint16).astype(np.int64)  # uint_cast
    sti &= ~MASK
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


def _get_events(raw, event_id):
    """Get events from STI channel, falling back to annotations."""
    if 'STI101' in raw.ch_names:
        return _decode_sti(raw)
    else:
        # No STI channel – events were saved as annotations.
        # Try matching annotation descriptions to numeric event codes.
        ev_id_str = {str(v): v for v in set(event_id.values())}
        events, _ = mne.events_from_annotations(raw, event_id=ev_id_str,
                                                verbose=False)
        return events


def _shift_evoked(evoked, delay_s):
    """Shift an Evoked's timeline earlier by delay_s (trigger→stimulus lag).

    Resamples each channel at times+delay_s but keeps the *same* nominal
    time axis, so every subject/site ends up on an identical time grid —
    required for later grand-averaging across subjects (mne.grand_average
    requires exact time-axis matches).
    """
    times = evoked.times
    src_times = times + delay_s
    evoked.data = np.array([np.interp(src_times, times, ch) for ch in evoked.data])
    return evoked


def compute_evoked_sub(fif_path, event_id, tmin, tmax,
                       l_freq=0.5, h_freq=30.0, recode=None, modality=None):
    """Return per-condition Evoked objects for one subject.

    modality: optional {condition_label: 'auditory'|'visual'}. If given,
    each condition's evoked is corrected for the measured trigger→stimulus
    delay (see trigger_delay_measurements/), which is site- and
    modality-specific. Epochs are extracted with extra tmax padding so the
    correction never has to extrapolate past the epoched data.
    """
    try:
        # Load full raw (keep STI channel) so _get_events can use it.
        raw = mne.io.read_raw_fif(fif_path, preload=True, verbose=False)
        raw.filter(l_freq, h_freq, picks='grad', verbose=False)
        events = _get_events(raw, event_id)
        raw.pick('grad')   # drop non-grad channels after event extraction
        if recode:
            # recode: {new_int: [list of old ints]}
            for new_code, old_codes in recode.items():
                events[np.isin(events[:, 2], old_codes), 2] = new_code
        epoch_tmax = tmax + _DELAY_PAD_S if modality else tmax
        epochs = mne.Epochs(raw, events, event_id=event_id,
                            tmin=tmin, tmax=epoch_tmax, baseline=(None, 0),
                            preload=True, verbose=False,
                            reject_by_annotation=True)
        scanner = SCANNER_MAP.get(_recording_key(fif_path)) if modality else None
        out = {}
        for cond in event_id:
            if cond in epochs.event_id and len(epochs[cond]) > 0:
                evoked = epochs[cond].average()
                mod = modality.get(cond) if modality else None
                if mod and scanner and (scanner, mod) in DELAYS_S:
                    evoked = _shift_evoked(evoked, DELAYS_S[(scanner, mod)])
                if modality:
                    evoked.crop(tmin, tmax)
                out[cond] = evoked
        return out
    except Exception as e:
        print(f'  skip {os.path.basename(fif_path)}: {type(e).__name__}: {e}')
        return {}


def compute_psd_sub(fif_path, fmin=1.0, fmax=40.0):
    """Return (dB PSD averaged over channels, freqs) for one resting-state file.

    Converting to dB per subject before group averaging gives the geometric
    mean across subjects, which is far less sensitive to high-power outliers
    than the arithmetic mean in linear space.
    """
    try:
        raw = mne.io.read_raw_fif(fif_path, preload=True, verbose=False)
        raw.pick('grad')
        sfreq = raw.info['sfreq']
        n_per_seg = int(4 * sfreq)
        try:  # MNE >= 1.0
            psd_obj = raw.compute_psd(method='welch', fmin=fmin, fmax=fmax,
                                      n_fft=n_per_seg, n_per_seg=n_per_seg,
                                      verbose=False)
            data, freqs = psd_obj.get_data(return_freqs=True)
        except AttributeError:  # MNE < 1.0
            data, freqs = mne.time_frequency.psd_welch(
                raw, fmin=fmin, fmax=fmax, n_fft=n_per_seg,
                n_per_seg=n_per_seg, verbose=False)
        lin = data.mean(axis=0) * 1e26  # (T/m)²/Hz → (fT/cm)²/Hz
        if PSD_STANDARDISE:
            lin = lin / lin.mean()
        return 10 * np.log10(np.maximum(lin, 1e-30)), freqs
    except Exception as e:
        print(f'  skip {os.path.basename(fif_path)}: {type(e).__name__}: {e}')
        return None, None


# ── helpers ───────────────────────────────────────────────────────────────────

def _subject_id(fif_path):
    """Extract subject ID (e.g. 'C1001', 'P2002') from a preprocessed fif path."""
    return os.path.basename(fif_path).split('_')[0]


_REC_RE = re.compile(r'^([A-Z]\d+)_.+_(bl2?|tw|af2?)_tsss_preproc_raw\.fif$')


def _recording_key(fif_path):
    """(NTAD_ID, visit code) from a preprocessed fif path, for SCANNER_MAP."""
    m = _REC_RE.match(os.path.basename(fif_path))
    return m.groups() if m else None


_ntad_ids_set = set(ntad_ids)


# ── per-subject storage + deferred aggregation ────────────────────────────────
#
# process_task / process_psd store ALL computed subjects in the pkl so that
# ntad_ids filtering can be changed without recomputing.
# _agg_task / _agg_psd apply the filter at plot time.

def gfp(evoked):
    """Global Field Power in fT/cm (gradiometers)."""
    return np.sqrt(np.mean(evoked.data ** 2, axis=0)) * 1e15


def process_task(files, event_id, tmin, tmax, recode=None, modality=None):
    """Return per-subject GFP arrays and evoked objects keyed by condition."""
    sub_evos = Parallel(n_jobs=N_JOBS, verbose=0)(
        delayed(compute_evoked_sub)(f, event_id, tmin, tmax, recode=recode,
                                    modality=modality)
        for f in files)
    sub_ids = [_subject_id(f) for f in files]

    result = {}
    for cond in event_id:
        items = [(sub_ids[i], sub_evos[i][cond])
                 for i in range(len(sub_evos)) if cond in sub_evos[i]]
        if not items:
            continue
        ids, evos = zip(*items)
        gfps  = np.array([gfp(e) for e in evos])
        times = evos[0].times
        # Baseline-correct per subject to remove noise-floor offset across conditions
        gfps -= gfps[:, times < 0].mean(axis=1, keepdims=True)
        result[cond] = dict(
            sub_ids = list(ids),
            gfps    = gfps,         # (n_subs, n_times) — baseline-corrected
            evokeds = list(evos),   # per-subject Evoked — needed for grand avg
            times   = times,
        )
    return result


def process_psd(files):
    """Return per-subject dB PSD arrays (for deferred filtering by ntad_ids)."""
    results = Parallel(n_jobs=N_JOBS, verbose=0)(
        delayed(compute_psd_sub)(f) for f in files)
    sub_ids = [_subject_id(f) for f in files]
    valid = [(sub_ids[i], results[i][0], results[i][1])
             for i in range(len(results)) if results[i][0] is not None]
    if not valid:
        return None
    ids, psds_db, freqs_list = zip(*valid)
    return dict(
        sub_ids = list(ids),
        psds_db = np.array(psds_db),   # (n_subs, n_freqs) — already in dB
        freqs   = freqs_list[0],
    )


def _per_subject_mean(sub_ids, data_rows, valid_set):
    """Return (array of per-subject means, list of unique valid subject IDs).

    Subjects with multiple recordings (visits) are averaged together so that
    every unique subject contributes exactly once to the group stats.
    """
    from collections import defaultdict
    buckets = defaultdict(list)
    for sid, row in zip(sub_ids, data_rows):
        if sid in valid_set:
            buckets[sid].append(row)
    if not buckets:
        return None, []
    ids   = sorted(buckets.keys())
    means = np.array([np.mean(buckets[sid], axis=0) for sid in ids])
    return means, ids


def _agg_task(raw, valid_set):
    """Aggregate task data to one observation per valid subject (averaged across visits).

    Handles both new format (sub_ids present) and old group-level format.
    """
    first = next(iter(raw.values()), {})
    if 'sub_ids' not in first:
        return raw  # old format: already group-level, use as-is
    out = {}
    for cond, d in raw.items():
        per_sub_gfps, ids = _per_subject_mean(d['sub_ids'], d['gfps'], valid_set)
        if per_sub_gfps is None:
            continue
        # For the grand average, average evokeds within each subject first
        from collections import defaultdict
        evo_buckets = defaultdict(list)
        for sid, evo in zip(d['sub_ids'], d['evokeds']):
            if sid in valid_set:
                evo_buckets[sid].append(evo)
        per_sub_evos = [mne.grand_average(evo_buckets[sid]) for sid in ids]
        out[cond] = dict(
            grand_avg = mne.grand_average(per_sub_evos),
            gfp_mean  = per_sub_gfps.mean(axis=0),
            gfp_sem   = per_sub_gfps.std(axis=0, ddof=1) / np.sqrt(len(ids)),
            times     = d['times'],
            n         = len(ids),
        )
    return out


def _agg_psd(raw, valid_set):
    """Aggregate PSD data to one observation per valid subject (averaged across visits).

    Handles both new format (sub_ids present) and old group-level format.
    """
    if raw is None:
        return None
    if 'sub_ids' not in raw:
        return raw  # old format: already group-level, use as-is
    per_sub, ids = _per_subject_mean(raw['sub_ids'], raw['psds_db'], valid_set)
    if per_sub is None:
        return None
    return dict(
        psd_mean = per_sub.mean(axis=0),
        psd_sem  = per_sub.std(axis=0, ddof=1) / np.sqrt(len(ids)),
        freqs    = raw['freqs'],
        n        = len(ids),
    )


# ── session definitions ───────────────────────────────────────────────────────
# Each entry: key → (label, compute_fn)
# compute_fn takes no arguments and returns the result dict for that session.

def _session_specs():
    return [
        ('t1', 'Task 1 – Audio-Visual',
         lambda: process_task(
             sorted(glob(f'{BASE}/1/tsss/*/*_preproc_raw.fif')),
             event_id={'Auditory': 22, 'Visual': 33},
             tmin=-0.2, tmax=0.5,
             modality={'Auditory': 'auditory', 'Visual': 'visual'})),
        ('t2', 'Task 2 – Mismatch Negativity',
         lambda: process_task(
             sorted(glob(f'{BASE}/2/tsss/*/*_preproc_raw.fif')),
             # Events: 100 = Deviant; 101-110 = Repetitions, recoded → 101
             event_id={'Deviant': 100, 'Standard': 101},
             tmin=-0.2, tmax=0.5,
             recode={101: list(range(101, 111))},
             modality={'Deviant': 'auditory', 'Standard': 'auditory'})),
        ('t3', 'Task 3 – Scene Repetition',
         lambda: process_task(
             sorted(glob(f'{BASE}/3/tsss/*/*_preproc_raw.fif')),
             # Events: 22 = Novel (first presentation), 33 = Familiar (repeated)
             event_id={'Novel': 22, 'Familiar': 33},
             tmin=-0.2, tmax=0.7,
             modality={'Novel': 'visual', 'Familiar': 'visual'})),
        ('t4', 'Task 4 – Visual-Auditory Oddball',
         lambda: process_task(
             sorted(glob(f'{BASE}/4/tsss/*vao_task*/*_preproc_raw.fif')),
             # Epoch around VISUAL trigger: visual response 0–300 ms,
             # auditory response 330–700 ms (audio fires 330 ms after visual).
             # Visual triggers: 10 = STD, 20 = AD, 30 = ND
             event_id={'Standard': 10, 'Aud. deviant': 20, 'Novel deviant': 30},
             tmin=-0.2, tmax=0.8,
             # Epoch is anchored to the visual trigger, so it is the visual
             # delay that must be corrected for.
             modality={'Standard': 'visual', 'Aud. deviant': 'visual',
                       'Novel deviant': 'visual'})),
        ('rso', 'Resting – Eyes Open',
         lambda: process_psd(
             sorted(glob(f'{BASE}/5/tsss/*/*_preproc_raw.fif')))),
        ('rsc', 'Resting – Eyes Closed',
         lambda: process_psd(
             sorted(glob(f'{BASE}/6/tsss/*/*_preproc_raw.fif')))),
    ]


def _session_pkl(key):
    return f'{OUT}/group_{key}.pkl'


def _is_new_format(result):
    """True if the pkl was saved in the per-subject format (has 'sub_ids')."""
    if result is None:
        return True  # None is valid (no data)
    if isinstance(result, dict):
        # Task pkl: dict keyed by condition, each value has 'sub_ids'
        first = next(iter(result.values()), None)
        if first is not None and isinstance(first, dict):
            return 'sub_ids' in first
        # PSD pkl: top-level has 'sub_ids'
        return 'sub_ids' in result
    return False


def load_or_compute(key, label, compute_fn, overwrite):
    """Load a session from cache or (re)compute it. Returns (result, was_computed)."""
    pth = _session_pkl(key)
    if not overwrite and os.path.exists(pth):
        with open(pth, 'rb') as fh:
            result = pickle.load(fh)
        if _is_new_format(result):
            print(f'  [cached]  {label}')
            return result, False
        print(f'  [stale format, recomputing] {label}')
    print(f'  [compute] {label}')
    result = compute_fn()
    with open(pth, 'wb') as fh:
        pickle.dump(result, fh)
    return result, True


# ── helpers ───────────────────────────────────────────────────────────────────

def _prep_scaled_freq(base, freq_vect):
    """Scale frequency axis for plotting (base=0.5 → sqrt-f axis).

    Returns (fx, ftick, ftickscaled) matching osl_ephys.glm.prep_scaled_freq.
    """
    fx = freq_vect ** base
    if base < 1:
        nticks = int(np.floor(freq_vect[-1] ** base))
        ftick = np.array([ii ** (1.0 / base) for ii in range(1, nticks + 1)])
        ftickscaled = ftick ** base
    else:
        ftick = None
        ftickscaled = None
    return fx, ftick, ftickscaled


# ── plotting ──────────────────────────────────────────────────────────────────

PALETTE = {
    'Auditory':       '#d62728',
    'Visual':         '#1f77b4',
    'Deviant':        '#d62728',
    'Standard':       '#1f77b4',
    'Novel':          '#d62728',
    'Familiar':       '#1f77b4',
    'Aud. deviant':   '#d62728',
    'Novel deviant':  '#2ca02c',
}


_DIFF_COLORS = ['#333333', '#777777']
_DIFF_STYLES = ['--', ':']


def plot_task_panel(ax, task_res, title, panel_label,
                    diff_pairs=None, vline_330=False, legend_loc='upper right',
                    legend_labels=None):
    """Plot GFP mean ± SEM; diff waves on right y-axis with independent scaling.

    legend_labels: optional {condition: display name} override for the legend
    text (defaults to the condition key itself).
    """
    for cond, d in task_res.items():
        t     = d['times'] * 1000
        color = PALETTE.get(cond, 'gray')
        disp  = legend_labels.get(cond, cond) if legend_labels else cond
        ax.plot(t, d['gfp_mean'], color=color, lw=1.5,
                label=f"{disp} (n={d['n']})")
        ax.fill_between(t,
                        d['gfp_mean'] - d['gfp_sem'],
                        d['gfp_mean'] + d['gfp_sem'],
                        alpha=0.2, color=color)

    ax.axvline(0, color='k', lw=0.8, ls='--', alpha=0.4)
    main_lines, main_labels = ax.get_legend_handles_labels()
    diff_lines, diff_labels = [], []

    if diff_pairs:
        ax_r = ax.twinx()
        all_diff_vals = []
        for i, (cond_a, cond_b) in enumerate(diff_pairs):
            if cond_a not in task_res or cond_b not in task_res:
                continue
            diff_ev = mne.combine_evoked(
                [task_res[cond_a]['grand_avg'], task_res[cond_b]['grand_avg']],
                weights=[1, -1])
            t    = diff_ev.times * 1000
            dgfp = gfp(diff_ev)
            col  = _DIFF_COLORS[i % len(_DIFF_COLORS)]
            ls   = _DIFF_STYLES[i % len(_DIFF_STYLES)]
            line, = ax_r.plot(t, dgfp, color=col, lw=1.2, ls=ls, alpha=0.85)
            diff_lines.append(line)
            diff_labels.append(f'{cond_a}−{cond_b}')
            all_diff_vals.append(dgfp)

        if all_diff_vals:
            all_v = np.concatenate(all_diff_vals)
            vmin, vmax = all_v.min(), all_v.max()
            pad = max(0.3 * (vmax - vmin), 0.1 * max(abs(vmin), abs(vmax)))
            ax_r.set_ylim(vmin - pad, vmax + pad)
        ax_r.set_ylabel('Diff GFP (fT/cm)', fontsize=8, color=_DIFF_COLORS[0])
        ax_r.tick_params(axis='y', labelcolor=_DIFF_COLORS[0], labelsize=7)

    if vline_330:
        ax.axvline(330, color='dimgray', lw=0.8, ls=':', alpha=0.5)

    # Clip x to first/last data point
    if task_res:
        t_ref = next(iter(task_res.values()))['times']
        ax.set_xlim(t_ref[0] * 1000, t_ref[-1] * 1000)

    # Extend top ylim and place 'aud. onset' label in the new headroom
    if vline_330:
        ymin, ymax = ax.get_ylim()
        pad = (ymax - ymin) * 0.18
        ax.set_ylim(ymin, ymax + pad)
        ax.text(335, ymax + pad * 0.45, 'auditory onset',
                ha='left', va='center', fontsize=6.5, color='dimgray')
        ax.text(5, ymax + pad * 0.45, 'visual onset',
                            ha='left', va='center', fontsize=6.5, color='dimgray')

    ax.set_title(title, fontweight='bold', fontsize=10)
    ax.set_xlabel('Time (ms)', fontsize=9)
    ax.set_ylabel('GFP (fT/cm)', fontsize=9)
    ax.legend(main_lines + diff_lines, main_labels + diff_labels,
              fontsize=7.5, loc=legend_loc, framealpha=0.7)
    ax.text(-0.05, 1.04, panel_label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='bottom', ha='right')


AGG_PKL = f'{OUT}/figure_data.pkl'


def compute_agg(res):
    """Aggregate per-subject session results to the group-level data actually
    plotted in the figure. Cheap relative to compute_evoked_sub/compute_psd_sub,
    but still touches every subject's Evoked objects — cached separately (see
    AGG_PKL) so cosmetic-only figure tweaks don't need to reload/re-aggregate
    the (much larger) per-subject pkls.
    """
    return {
        't1':  _agg_task(res['t1'],  _ntad_ids_set),
        't2':  _agg_task(res['t2'],  _ntad_ids_set),
        't3':  _agg_task(res['t3'],  _ntad_ids_set),
        't4':  _agg_task(res['t4'],  _ntad_ids_set),
        'rso': _agg_psd(res['rso'],  _ntad_ids_set),
        'rsc': _agg_psd(res['rsc'],  _ntad_ids_set),
    }


def plot_figure(agg):
    fig = plt.figure(figsize=(12, 9))
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.5, wspace=0.32)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    ax5 = fig.add_subplot(gs[2, 0])

    plot_task_panel(ax1, agg['t1'],
                    'Task 1: Audio-Visual', 'a')
    plot_task_panel(ax2, agg['t2'],
                    'Task 2: Mismatch Negativity', 'b',
                    # diff_pairs=[('Deviant', 'Standard')]
                    )
    plot_task_panel(ax3, agg['t3'],
                    'Task 3: Scene Repetition', 'c',
                    # diff_pairs=[('Novel', 'Familiar')]
                    )
    plot_task_panel(ax4, agg['t4'],
                    'Task 4: Visual-Auditory Oddball', 'd',
                    # diff_pairs=[('Standard', 'Aud. deviant'),
                    #             ('Standard', 'Novel deviant')],
                    vline_330=True,
                    legend_loc='lower center',
                    legend_labels={'Standard':      'Standard sound',
                                   'Aud. deviant':  'Mismatch sound',
                                   'Novel deviant': 'Novel sound'})

    # Resting-state PSD. psd_mean/psd_sem are already in dB — computed
    # per-subject in compute_psd_sub, so the group mean is a geometric mean.
    freqs_ref = None
    for key, label, color in [('rso', 'Eyes open',   '#1f77b4'),
                               ('rsc', 'Eyes closed', '#d62728')]:
        d = agg[key]
        if d is None:
            continue
        freqs_ref = d['freqs']
        db     = d['psd_mean']   # already in dB
        db_sem = d['psd_sem']
        fx, _, _ = _prep_scaled_freq(PSD_AX, freqs_ref)
        ax5.plot(fx, db, color=color, lw=1.5,
                 label=f'{label} (n={d["n"]})')
        ax5.fill_between(fx, db - db_sem, db + db_sem, alpha=0.2, color=color)

    if freqs_ref is not None:
        fx_ref, ftick, ftickscaled = _prep_scaled_freq(PSD_AX, freqs_ref)
        if ftick is not None:
            ax5.set_xticks(ftickscaled)
            ax5.set_xticklabels([str(int(t)) for t in ftick])
        ax5.set_xlim(fx_ref[0], fx_ref[-1])
        alpha_lo, alpha_hi = 7 ** PSD_AX, 13 ** PSD_AX
        ax5.axvspan(alpha_lo, alpha_hi, alpha=0.10, color='gray',
                    zorder=0, label='Alpha (7–13 Hz)')
        ylim = ax5.get_ylim()
        ax5.text((alpha_lo + alpha_hi) / 2, ylim[1] * 0.98, 'α',
                 ha='center', va='top', fontsize=11, color='gray', alpha=0.8)

    ylabel = ('Standardised Power (dB)' if PSD_STANDARDISE
              else 'Power (dB re. (fT/cm)²/Hz)')
    ax5.set_xlabel('Frequency (Hz)', fontsize=9)
    ax5.set_ylabel(ylabel, fontsize=9)
    ax5.set_title('Resting State: Power Spectral Density',
                  fontweight='bold', fontsize=10)
    ax5.legend(fontsize=9, framealpha=0.7)
    ax5.text(-0.03, 1.04, 'e', transform=ax5.transAxes,
             fontsize=12, fontweight='bold', va='bottom', ha='right')

    for fmt in ('png', 'pdf'):
        path = f'{OUT}/technical_validation.{fmt}'
        fig.savefig(path, dpi=300, bbox_inches='tight', pad_inches=0.05)
        print(f'Saved → {path}')
    plt.close(fig)


# ── event table ──────────────────────────────────────────────────────────────

def make_event_table():
    """Save event details table to CSV and print to stdout.

    Counts are the programmed number of trials per full session, derived from
    the Presentation experiment files shipped with the dataset.

    STI channel reading for all tasks (see _decode_sti):
        STI101 cast to uint16 (corrects a Neuromag STI016 signed-integer
        acquisition bug), sync bits masked out (mask = 256 | 4096, Oxford |
        Cambridge site-sync pulses), then decoded pulse by pulse: a bit is
        part of the code if it is high for >= 75% of the pulse. This equals
        mne.find_events(mask=4352, mask_type='not_and', uint_cast=True) on
        clean recordings and corrects the chattering trigger bit on the
        Cambridge Triux Neo.
    """
    READING = ("STI101; uint16 cast; mask=4352 (256|4096) removed; code = bits "
               "high for >=75% of each pulse")

    # Timing values derived from Presentation experiment files (.sce / .tem).
    # All times in milliseconds.
    #
    # Task 1 (AV, unimodalav): avtask.tem
    #   picture + sound both at time=0 (simultaneous), picdur=300 ms
    #   fixation cross from t=300 ms for crossdur = trdur-300 ms (jittered)
    #   trdur: 1205-3397 ms (mean ~2261 ms); crossdur: 905-3097 ms (mean ~1961 ms)
    #
    # Task 2 (Roving MMN): roving.tem
    #   Continuous tone sequence embedded in a video; no per-trial start.
    #   nothing at deltat=0, tone at deltat=500 ms, tone duration=100 ms.
    #   SOA ~500 ms (fixed); ISI ~400 ms.
    #
    # Task 3 (Scene Repetition): scenes.tem
    #   Fixation cross: 0-300 ms; scene image: 300-1100 ms (trigger at 300 ms);
    #   post-image fixation: jitter ms (3-200 ms, mean ~100 ms, uniform).
    #   trdur: 1103-1300 ms (mean ~1200 ms).
    #
    # Task 4 (VAO): vao_train.tem
    #   Visual image: t=0-700 ms (trigger at t=0).
    #   Audio: deltat=300 ms from image onset; t=300-700 ms (trigger at t=300 ms).
    #   Post-stimulus blank: crossdur = trdur-700 ms (jittered, 200-400 ms, mean ~304 ms).
    #   trdur: 900-1100 ms (mean ~1004 ms).

    _AV   = ('0',          '300',                         '905-3097 (jittered, mean ~1961)')
    _MMN  = ('SOA ~500',   '100',                         '~400 (fixed)')
    _SCEN = ('300',        '800',                         '3-200 (jittered, mean ~100)')
    _VAO  = ('0 (vis.) / +300 (aud.)', '700 (vis.) / 400 (aud.)', '200-400 (jittered, mean ~304)')

    rows = [
        # (session, task, condition, trigger_code, N, used, notes, timing)
        # timing = (_AV / _MMN / _SCEN / _VAO) tuple
        # ── Task 1: Audio-Visual ──────────────────────────────────────────────
        (1, 'Audio-Visual', 'Auditory',             '22',  100, True,  '',                              _AV),
        (1, 'Audio-Visual', 'Visual',               '33',  100, True,  '',                              _AV),
        (1, 'Audio-Visual', 'Filler',               '55',   30, False, 'Silent filler; not analysed',   _AV),
        # ── Task 2: Roving MMN ───────────────────────────────────────────────
        # 6 blocks total (rov1-1 … rov3-2).  Standards 101–111 recoded to 101.
        (2, 'Roving MMN', 'Deviant',               '100', 246, True,  '',                              _MMN),
        (2, 'Roving MMN', 'Standard (position 1)', '101', 246, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 2)', '102', 240, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 3)', '103', 228, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 4)', '104', 216, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 5)', '105', 186, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 6)', '106', 156, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 7)', '107', 126, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 8)', '108',  96, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 9)', '109',  66, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 10)','110',  36, True,  'Recoded to 101 for analysis',   _MMN),
        (2, 'Roving MMN', 'Standard (position 11)','111',  18, True,  'Recoded to 101 for analysis',   _MMN),
        # ── Task 3: Scene Repetition ──────────────────────────────────────────
        (3, 'Scene Repetition', 'Novel',            '22', 280, True,  '',                              _SCEN),
        (3, 'Scene Repetition', 'Familiar',         '33', 256, True,  '',                              _SCEN),
        (3, 'Scene Repetition', 'Moon filler',      '11',  26, False, 'Filler image; not analysed',    _SCEN),
        # ── Task 4: Visual-Auditory Oddball ───────────────────────────────────
        # Visual trigger at t=0 ms; audio trigger at t=+300 ms.
        # Epochs are aligned to the visual trigger.
        (4, 'VAO', 'Standard',              '10 / 11',  670, True,  'Visual / audio onset (+300 ms)', _VAO),
        (4, 'VAO', 'Auditory deviant',      '20 / 22',   50, True,  'Visual / audio onset (+300 ms)', _VAO),
        (4, 'VAO', 'Novel deviant',         '30 / 33',   50, True,  'Visual / audio onset (+300 ms)', _VAO),
        (4, 'VAO', 'Target (button press)', '90 / 99',   40, False, 'Visual / audio; not analysed',   _VAO),
    ]

    headers = [
        'Session', 'Task', 'Condition',
        'Trigger code (STI101)', 'N trials (per session)',
        'Used in analysis',
        'Trigger onset in trial (ms)',
        'Stimulus duration (ms)',
        'Post-stimulus ISI (ms)',
        'Notes', 'STI channel reading',
    ]

    csv_path = f'{OUT}/event_table.csv'
    with open(csv_path, 'w', newline='') as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        for r in rows:
            writer.writerow([r[0], r[1], r[2], r[3], r[4],
                             'yes' if r[5] else 'no',
                             r[7][0], r[7][1], r[7][2],
                             r[6], READING])
    print(f'Event table → {csv_path}')

    # Pretty-print to stdout (omit STI reading column to keep width manageable)
    flat = [(r[0], r[1], r[2], r[3], r[4],
             'yes' if r[5] else 'no',
             r[7][0], r[7][1], r[7][2], r[6])
            for r in rows]
    print_headers = headers[:-1]  # omit STI column from terminal output
    widths = [max(len(str(row[i])) for row in flat + [tuple(print_headers)])
              for i in range(len(print_headers))]
    sep = '+' + '+'.join('-' * (w + 2) for w in widths) + '+'

    def _fmt(row):
        return '|' + '|'.join(f' {str(v):<{w}} ' for v, w in zip(row, widths)) + '|'

    print(sep)
    print(_fmt(print_headers))
    print(sep)
    for row in flat:
        print(_fmt(row))
    print(sep)
    print(f'\nSTI channel reading (all tasks): {READING}')


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='NTAD MEG technical validation figure')
    parser.add_argument(
        '--overwrite', action='store_true',
        help='Recompute all sessions even if cached pkl files already exist')
    parser.add_argument(
        '--sessions', nargs='*',
        metavar='SESSION',
        help='Recompute only these sessions (e.g. --sessions t1 rso). '
             'Implies overwrite for the listed sessions only.')
    parser.add_argument(
        '--plot-only', action='store_true',
        help='Skip all computation; load existing pkls as-is and regenerate figure.')
    parser.add_argument(
        '--table-only', action='store_true',
        help='Print and save the event table without loading any session data.')
    parser.add_argument(
        '--figure-only', action='store_true',
        help='Redraw the figure from the cached plot-ready data '
             f'({AGG_PKL}) without touching any per-subject pkl. '
             'Fastest option for cosmetic-only changes (labels, layout, colours).')
    args = parser.parse_args()

    if args.table_only:
        make_event_table()
        raise SystemExit(0)

    if args.figure_only:
        if not os.path.exists(AGG_PKL):
            raise SystemExit(
                f'{AGG_PKL} not found — run once without --figure-only first.')
        print(f'  [load]    {AGG_PKL}')
        with open(AGG_PKL, 'rb') as fh:
            agg = pickle.load(fh)
        print('Generating figure…')
        plot_figure(agg)
        raise SystemExit(0)

    specs = _session_specs()
    total = len(specs)
    res   = {}

    if args.plot_only:
        for key, label, _ in specs:
            pth = _session_pkl(key)
            if os.path.exists(pth):
                print(f'  [load]    {label}')
                with open(pth, 'rb') as fh:
                    res[key] = pickle.load(fh)
            else:
                print(f'  [missing] {label}')
                res[key] = None
    else:
        any_new = False
        for i, (key, label, compute_fn) in enumerate(specs, 1):
            ow = args.overwrite or (args.sessions is not None and key in args.sessions)
            print(f'[{i}/{total}] {label}')
            res[key], was_computed = load_or_compute(key, label, compute_fn, ow)
            any_new = any_new or was_computed

    agg = compute_agg(res)
    with open(AGG_PKL, 'wb') as fh:
        pickle.dump(agg, fh)

    print('Generating figure…')
    plot_figure(agg)

    print('\nEvent table:')
    make_event_table()
