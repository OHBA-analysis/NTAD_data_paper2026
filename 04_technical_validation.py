#!/usr/bin/env python3
"""
Technical validation figure for NTAD MEG dataset (Nature Data paper).

Four tasks (evoked responses) + resting state (power spectra).
Results are cached to a pickle so plotting can be re-run independently.
"""

import os
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
PSD_AX = 0.5  # sqrt(f) axis for PSD plot (1.0 = linear, 0.5 = sqrt, 2.0 = f²)

# ── per-subject helpers ───────────────────────────────────────────────────────
df=pd.read_csv('/ohba/pi/mwoolrich/datasets/ntad/DataPortalIngest_March2025/ParticipantOverview.csv')
ntad_ids = list(df[df['analyseable_using_NTAD_criteria']=='Yes']['NTAD_ID'].unique())


def _get_events(raw, event_id):
    """Get events from STI channel, falling back to annotations."""
    try:
        return mne.find_events(raw, shortest_event=1, mask=MASK,
                               mask_type=MASK_TYPE, uint_cast=True,
                               verbose=False)
    except ValueError:
        # No STI channel – events were saved as annotations.
        # Try matching annotation descriptions to numeric event codes.
        ev_id_str = {str(v): v for v in set(event_id.values())}
        events, _ = mne.events_from_annotations(raw, event_id=ev_id_str,
                                                verbose=False)
        return events


def compute_evoked_sub(fif_path, event_id, tmin, tmax,
                       l_freq=0.5, h_freq=30.0, recode=None):
    """Return per-condition Evoked objects for one subject."""
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
        epochs = mne.Epochs(raw, events, event_id=event_id,
                            tmin=tmin, tmax=tmax, baseline=(None, 0),
                            preload=True, verbose=False,
                            reject_by_annotation=True)
        out = {}
        for cond in event_id:
            if cond in epochs.event_id and len(epochs[cond]) > 0:
                out[cond] = epochs[cond].average()
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


_ntad_ids_set = set(ntad_ids)


# ── per-subject storage + deferred aggregation ────────────────────────────────
#
# process_task / process_psd store ALL computed subjects in the pkl so that
# ntad_ids filtering can be changed without recomputing.
# _agg_task / _agg_psd apply the filter at plot time.

def gfp(evoked):
    """Global Field Power in fT/cm (gradiometers)."""
    return np.sqrt(np.mean(evoked.data ** 2, axis=0)) * 1e15


def process_task(files, event_id, tmin, tmax, recode=None):
    """Return per-subject GFP arrays and evoked objects keyed by condition."""
    sub_evos = Parallel(n_jobs=N_JOBS, verbose=0)(
        delayed(compute_evoked_sub)(f, event_id, tmin, tmax, recode=recode)
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
             tmin=-0.2, tmax=0.5)),
        ('t2', 'Task 2 – Mismatch Negativity',
         lambda: process_task(
             sorted(glob(f'{BASE}/2/tsss/*/*_preproc_raw.fif')),
             # Events: 100 = Deviant; 101-110 = Repetitions, recoded → 101
             event_id={'Deviant': 100, 'Standard': 101},
             tmin=-0.2, tmax=0.5,
             recode={101: list(range(101, 111))})),
        ('t3', 'Task 3 – Scene Repetition',
         lambda: process_task(
             sorted(glob(f'{BASE}/3/tsss/*/*_preproc_raw.fif')),
             # Events: 22 = Novel (first presentation), 33 = Familiar (repeated)
             event_id={'Novel': 22, 'Familiar': 33},
             tmin=-0.2, tmax=0.7)),
        ('t4', 'Task 4 – Visual-Auditory Oddball',
         lambda: process_task(
             sorted(glob(f'{BASE}/4/tsss/*vao_task*/*_preproc_raw.fif')),
             # Epoch around VISUAL trigger: visual response 0–300 ms,
             # auditory response 330–700 ms (audio fires 330 ms after visual).
             # Visual triggers: 10 = STD, 20 = AD, 30 = ND
             event_id={'Standard': 10, 'Aud. deviant': 20, 'Novel deviant': 30},
             tmin=-0.2, tmax=0.8)),
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
                    diff_pairs=None, vline_330=False, legend_loc='upper right'):
    """Plot GFP mean ± SEM; diff waves on right y-axis with independent scaling."""
    for cond, d in task_res.items():
        t     = d['times'] * 1000
        color = PALETTE.get(cond, 'gray')
        ax.plot(t, d['gfp_mean'], color=color, lw=1.5,
                label=f"{cond} (n={d['n']})")
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
        ax.text(335, ymax + pad * 0.45, 'aud. onset',
                ha='left', va='center', fontsize=6.5, color='dimgray')

    ax.set_title(title, fontweight='bold', fontsize=10)
    ax.set_xlabel('Time (ms)', fontsize=9)
    ax.set_ylabel('GFP (fT/cm)', fontsize=9)
    ax.legend(main_lines + diff_lines, main_labels + diff_labels,
              fontsize=7.5, loc=legend_loc, framealpha=0.7)
    ax.text(-0.05, 1.04, panel_label, transform=ax.transAxes,
            fontsize=12, fontweight='bold', va='bottom', ha='right')


def make_figure(res):
    # Aggregate to valid subjects only — cheap, no recomputation needed
    agg = {
        't1':  _agg_task(res['t1'],  _ntad_ids_set),
        't2':  _agg_task(res['t2'],  _ntad_ids_set),
        't3':  _agg_task(res['t3'],  _ntad_ids_set),
        't4':  _agg_task(res['t4'],  _ntad_ids_set),
        'rso': _agg_psd(res['rso'],  _ntad_ids_set),
        'rsc': _agg_psd(res['rsc'],  _ntad_ids_set),
    }

    fig = plt.figure(figsize=(14, 11))
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.55, wspace=0.38)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    ax5 = fig.add_subplot(gs[2, :])

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
                    legend_loc='lower center')

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

    fig.suptitle('NTAD MEG Dataset – Technical Validation',
                 fontsize=13, y=1.01)

    for fmt in ('png', 'pdf'):
        path = f'{OUT}/technical_validation.{fmt}'
        fig.savefig(path, dpi=150, bbox_inches='tight')
        print(f'Saved → {path}')
    plt.close(fig)


# ── event table ──────────────────────────────────────────────────────────────

def make_event_table():
    """Save event details table to CSV and print to stdout.

    Counts are the programmed number of trials per full session, derived from
    the Presentation experiment files shipped with the dataset.

    STI channel reading for all tasks:
        mne.find_events(raw, stim_channel='STI101',
                        mask=4352, mask_type='not_and',
                        uint_cast=True, shortest_event=1)
    mask = 256 | 4096 (Oxford site-sync | Cambridge site-sync pulses);
    mask_type='not_and' passes events that have *neither* sync bit set.
    uint_cast=True corrects a Neuromag STI016 signed-integer acquisition bug.
    """
    READING = "STI101; mask=4352 (256|4096), mask_type='not_and', uint_cast=True"

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
    args = parser.parse_args()

    if args.table_only:
        make_event_table()
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

    print('Generating figure…')
    make_figure(res)

    print('\nEvent table:')
    make_event_table()
