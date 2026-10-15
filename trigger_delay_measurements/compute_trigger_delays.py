"""Infer the lag between a digital STI101 trigger code and the actual
stimulus onset (audio or photodiode) recorded on an analog MISC channel.

Trigger codes and what they mean were confirmed against the source
Presentation trial lists in meeg_experiment_scripts/av/ (not just the
downstream analysis-pipeline docs, which turned out to be right here but
shouldn't be trusted blindly):

  unimodalav_task_trials.txt columns (condition, trigger, soundfile):
    "aonly"  22  t300/t600/t1200   -> Auditory-only, a real tone plays
    "vonly"  33  silence           -> Visual-only, no sound
    "filler" 55  silence           -> Filler, no sound

  avtask_practice_trials.txt uses trigger=44 for "audiovis"/"vonly"/"aonly"
  ALIKE -- i.e. 44 is a practice-block marker that does NOT identify a
  specific modality and should not be treated as a clean condition.

Site differences:
  Oxford avtask/scenerep each export only one MISC channel (MISC012 audio,
  MISC011 photodiode respectively). Cambridge exports MISC001-012, but only
  MISC006/MISC007 show any trigger-locked signal at all.

This script went through several broken versions before this one, each
worth recording so the mistake isn't repeated:

  1. Trigger onsets were found by thresholding STI101's own amplitude at
     50% of its range. STI101 encodes several distinct integer codes, and
     that threshold silently dropped every code below half the channel's
     max value -- e.g. Oxford avtask's code=22 ("Auditory") was never seen,
     so the audio channel got tested against Visual/Filler trials with no
     sound and correctly found nothing.
  2. mne.Epochs' baseline=(None, 0) argument does NOT correct 'misc'-type
     channels -- confirmed in the installed mne (1.3.1) source:
     Epochs._detrend_picks calls _pick_data_channels(), which excludes
     'misc'. epochs.baseline still *reports* the requested window, so this
     fails silently. Without it, "evoked" was each channel's raw absolute
     level (e.g. ~1.06 V DC offset on Oxford's MISC012), and dividing that
     by a genuinely tiny baseline std produced enormous, meaningless "SNR"
     values regardless of whether any real response existed -- e.g. a
     Cambridge avtask Visual-only ("no sound") trial showed SNR=586 despite
     the underlying trace being a flat, featureless line with a slow linear
     drift, not a response. The fix is to always baseline-correct manually
     (subtract each epoch's own pre-trigger mean) after pulling data out of
     mne.Epochs, regardless of what `baseline=` was passed to the
     constructor -- see the line doing that explicitly below.

Add further entries to RUNS below to cover more sessions/sites.
"""

import os

import matplotlib
import matplotlib.pyplot as plt
import mne
import numpy as np

matplotlib.use('Agg')  # headless-safe; figures are saved to disk, not shown

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _slugify(label):
    keep = (c if c.isalnum() else ' ' for c in label.lower())
    return '_'.join(''.join(keep).split())


def _envelope(seg, sfreq, envelope_ms=3.0):
    """Rolling RMS envelope of a single trial's post-trigger segment.

    Used instead of the raw (oscillating) signal for onset detection: a
    single noisy sample can't masquerade as sustained signal in an RMS
    envelope the way it can in a raw threshold crossing.
    """
    win = max(1, int(envelope_ms / 1000 * sfreq))
    return np.sqrt(np.convolve(seg ** 2, np.ones(win) / win, mode='same'))


def _detect_onset(envelope, sfreq, threshold, min_consec_ms=5.0):
    """First point where `envelope` clears `threshold` and stays above it
    for at least min_consec_ms. Returns None if it never does -- i.e. this
    trial has no detectable response, which is the correct outcome for a
    genuinely non-responsive trial rather than forcing a (wrong) estimate.
    """
    above = envelope > threshold
    min_consec = max(1, int(min_consec_ms / 1000 * sfreq))
    for i in range(len(above) - min_consec):
        if above[i:i + min_consec].all():
            return (i + 1) / sfreq * 1000
    return None


def compute_lag(fif_path, trigger_code, signal_ch, label,
                 tmin=-0.05, tmax=0.4, snr_threshold=10.0,
                 envelope_ms=3.0, min_consec_ms=5.0, threshold_factor=0.3,
                 min_responsive_trials=5):
    """Stimulus-onset lag for a specific trigger code, using mne.Epochs
    throughout (correct first_samp handling) plus two independent checks:

      1. Grand-average (evoked) SNR gates whether a response exists at all
         in the population.
      2. Per-trial envelope-threshold detection (only if #1 passes)
         describes the lag distribution -- median, spread, and how many
         trials show an implausibly late "detection" (a sign of noise, not
         response). A trial counts as responsive iff detection succeeds.
    """
    raw = mne.io.read_raw(fif_path, preload=True, verbose=False)
    sfreq = raw.info['sfreq']
    events = mne.find_events(raw, shortest_event=1, verbose=False)

    print(f"\n=== {label} ===")
    print(f"  File          : {fif_path}")

    # baseline=(None, 0) here does NOT correct MISC-type channels -- MNE's
    # Epochs restricts detrend/baseline correction to "data channels" (MEG/
    # EEG/aux) via its internal _detrend_picks, silently skipping 'misc'.
    # Confirmed by inspecting mne.epochs._pick_data_channels: 'misc' is not
    # included even though epochs.baseline reports the requested window.
    # So this must be done manually below regardless of that parameter.
    epochs = mne.Epochs(raw, events, event_id={'code': trigger_code},
                         tmin=tmin, tmax=tmax, baseline=(None, 0),
                         preload=True, verbose=False)
    data = epochs.get_data(picks=[signal_ch])[:, 0, :]  # (n_epochs, n_times)
    times_ms = epochs.times * 1000
    pre = (epochs.times < 0).sum()

    print(f"  Trigger code  : {trigger_code}  ({len(data)} epochs)")
    if len(data) == 0:
        print("  ERROR: no epochs found for this trigger code")
        return None

    data = data - data[:, :pre].mean(axis=1, keepdims=True)  # manual baseline correct
    evoked = data.mean(axis=0)
    evoked_baseline_std = evoked[:pre].std()
    snr = np.abs(evoked[pre:]).max() / evoked_baseline_std
    print(f"  evoked SNR    : {snr:.2f} (grand-average peak deviation / baseline noise)")

    # computed regardless of the SNR gate below so the diagnostic plot can
    # always show the sorted-by-variance trial image, even on failure
    post_var = data[:, pre:].var(axis=1)

    result, lags_ms, responsive = None, np.array([]), np.zeros(len(data), dtype=bool)

    if snr < snr_threshold:
        print(f"  ERROR: evoked SNR below {snr_threshold} -- no reliable "
              f"stimulus-locked response detected, not reporting a lag")
    else:
        envelopes = [_envelope(seg, sfreq, envelope_ms) for seg in data[:, pre:]]
        # ONE threshold for every trial, calibrated from the median of all
        # individual trials' own envelope peaks -- stable and representative
        # even with large trial-to-trial amplitude variation (unlike each
        # trial's own peak, or the grand-average's, see docstring point 5).
        global_thresh = threshold_factor * np.median([e.max() for e in envelopes])
        per_trial_lag = [_detect_onset(e, sfreq, global_thresh, min_consec_ms)
                          for e in envelopes]
        responsive = np.array([lag is not None for lag in per_trial_lag])
        lags_ms = np.array([lag for lag in per_trial_lag if lag is not None])

        print(f"  responsive    : {responsive.sum()} / {len(data)} trials "
              f"cleared the envelope-onset threshold")

        if len(lags_ms) < min_responsive_trials:
            print(f"  ERROR: only {len(lags_ms)} responsive trials with a "
                  f"detectable onset -- too few for a reliable estimate")
        else:
            late_lag_ms = 3 * np.median(lags_ms)
            n_late = (lags_ms > late_lag_ms).sum()
            result = float(np.median(lags_ms))
            print(f"  lags found    : {len(lags_ms)}")
            print(f"    median = {np.median(lags_ms):.2f} ms")
            print(f"    mean   = {lags_ms.mean():.2f} ms, std = {lags_ms.std():.2f} ms")
            print(f"    n > {late_lag_ms:.0f} ms (3x median) = {n_late} "
                  f"({100 * n_late / len(lags_ms):.0f}% -- likely mis-detections "
                  f"that caught a later feature instead of true onset)")
            if n_late / len(lags_ms) > 0.15:
                print(f"    WARNING: >15% of trials show implausibly late lags "
                      f"-- treat the median above as indicative, not calibrated")

    _plot_diagnostic(label, signal_ch, data, times_ms, pre, responsive, lags_ms,
                      result, post_var)
    return result


def _plot_diagnostic(label, signal_ch, data, times_ms, pre, responsive, lags_ms,
                      result, post_var):
    fig, axes = plt.subplots(4, 1, figsize=(13, 17),
                              gridspec_kw={'height_ratios': [2, 2, 3, 3]})
    fig.suptitle(label)

    axes[0].plot(times_ms, data.mean(axis=0), color='k', label='mean of all epochs')
    if responsive.sum():
        axes[0].plot(times_ms, data[responsive].mean(axis=0), color='r',
                     label=f'mean of {responsive.sum()} responsive epochs')
    axes[0].axvline(0, color='gray', linestyle=':')
    axes[0].set_xlabel('Time relative to trigger (ms)')
    axes[0].set_ylabel('Amplitude (baseline-corrected)')
    axes[0].legend()
    axes[0].set_title(f'{signal_ch}, n={len(data)} trigger(s)')

    if len(lags_ms):
        axes[1].hist(lags_ms, bins=min(30, max(5, len(lags_ms) // 2)), edgecolor='k')
        if result is not None:
            axes[1].axvline(result, color='r', linestyle='--',
                             label=f'median = {result:.1f} ms')
        axes[1].legend()
    axes[1].set_xlabel('Per-trial detected lag (ms)')
    axes[1].set_ylabel('Count')
    axes[1].set_title('Per-trial lag distribution (responsive trials only)')

    # Trial-by-trial image, sorted by post-trigger variance, with the
    # responsive/non-responsive cutoff and the estimated delay marked
    # directly on it -- lets you see at a glance whether the cutoff and lag
    # estimate actually land where the real response starts, rather than
    # trusting the summary numbers alone. Two versions: linear amplitude
    # (panel 3) shows the biggest tier clearly but can wash out smaller
    # real tiers as a uniform dark band (e.g. Cambridge avtask's ~0.003 and
    # ~0.02 tiers next to its ~0.6 one); log10(amplitude) (panel 4) keeps
    # all tiers visible at once at the cost of exaggerating baseline noise.
    n = len(data)
    order = np.argsort(post_var)
    amp = np.abs(data[order])
    n_responsive = int(responsive.sum())

    for ax, img, cbar_label in [(axes[2], amp, '|amplitude|'),
                                 (axes[3], np.log10(amp + 1e-12), 'log10(|amplitude|)')]:
        im = ax.imshow(img, aspect='auto', origin='upper',
                        extent=[times_ms[0], times_ms[-1], n, 0], cmap='viridis')
        if n_responsive:
            ax.axhline(n - n_responsive, color='r', linestyle='--', linewidth=1.5,
                       label=f'{n_responsive}/{n} responsive cutoff')
        if result is not None:
            ax.axvline(result, color='orange', linestyle='--', linewidth=1.5,
                       label=f'estimated delay = {result:.1f} ms')
        ax.axvline(0, color='white', linestyle=':', linewidth=1, alpha=0.7)
        ax.set_xlabel('Time relative to trigger (ms)')
        ax.set_ylabel('Trial (sorted by post-trigger variance,\nlow to high, top to bottom)')
        if n_responsive or result is not None:
            ax.legend(loc='upper right', fontsize=8)
        fig.colorbar(im, ax=ax, label=cbar_label)

    plt.tight_layout()

    out_path = os.path.join(SCRIPT_DIR, _slugify(label) + '.png')
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"  Figure saved to {out_path}")


RUNS = [
    dict(
        fif_path=os.path.join(SCRIPT_DIR, 'ntad_oxford_avtask.fif'),
        signal_ch='MISC012', trigger_code=22,
        label='Oxford avtask: Audio lag (code=22 Auditory, MISC012)',
    ),
    dict(
        fif_path=os.path.join(SCRIPT_DIR, 'ntad_oxford_scenerep.fif'),
        signal_ch='MISC011', trigger_code=33,
        label='Oxford scenerep: Photodiode lag (code=33, MISC011)',
    ),
    dict(
        fif_path=os.path.join(SCRIPT_DIR, 'ntad_cambridge_mmn.fif'),
        signal_ch='MISC006', trigger_code=100,
        label='Cambridge mmn: Audio lag (code=100 Deviant, MISC006)',
    ),
    dict(
        fif_path=os.path.join(SCRIPT_DIR, 'ntad_cambridge_avtask.fif'),
        signal_ch='MISC006', trigger_code=22,
        label='Cambridge avtask: Audio lag (code=22 Auditory, MISC006)',
    ),
    dict(
        fif_path=os.path.join(SCRIPT_DIR, 'ntad_cambridge_avtask.fif'),
        signal_ch='MISC006', trigger_code=33,
        label='Cambridge avtask: Photodiode check (code=33 Visual, MISC006)',
    ),
]


if __name__ == '__main__':
    results = {}
    for run in RUNS:
        if not os.path.exists(run['fif_path']):
            print(f"\nSkipping '{run['label']}': file not found ({run['fif_path']})")
            continue
        results[run['label']] = compute_lag(**run)

    print("\n=== SUMMARY ===")
    width = max(len(label) for label in results) if results else 0
    for label, lag_ms in results.items():
        value = f"{lag_ms:6.2f} ms" if lag_ms is not None else "FAILED"
        print(f"  {label:{width}s}: {value}")
