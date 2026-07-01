
import mne
import matplotlib.pyplot as plt
import numpy as np


def find_onsets(signal, sfreq, threshold_factor=0.5, min_gap_s=0.1):
    """Find rising-edge onset samples of a continuous signal."""
    threshold = threshold_factor * (signal.max() - signal.min()) + signal.min()
    above = signal > threshold
    rising = np.where(np.diff(above.astype(int)) == 1)[0] + 1
    # merge events closer than min_gap_s
    if len(rising) == 0:
        return rising
    min_gap = int(min_gap_s * sfreq)
    keep = [rising[0]]
    for r in rising[1:]:
        if r - keep[-1] > min_gap:
            keep.append(r)
    return np.array(keep)


def compute_lag(fif_path, trigger_ch, signal_ch, label):
    raw = mne.io.read_raw(fif_path, preload=True, verbose=False)
    sfreq = raw.info['sfreq']

    trig_idx = raw.ch_names.index(trigger_ch)
    sig_idx  = raw.ch_names.index(signal_ch)

    trig_data = raw._data[trig_idx]
    sig_data  = raw._data[sig_idx]

    trig_onsets = find_onsets(trig_data, sfreq, threshold_factor=0.5)
    sig_onsets  = find_onsets(sig_data,  sfreq, threshold_factor=0.5)

    print(f"\n=== {label} ===")
    print(f"  File       : {fif_path}")
    print(f"  sfreq      : {sfreq} Hz")
    print(f"  {trigger_ch} onsets : {len(trig_onsets)}")
    print(f"  {signal_ch} onsets : {len(sig_onsets)}")

    if len(trig_onsets) == 0 or len(sig_onsets) == 0:
        print("  ERROR: no onsets found — check threshold / channel data")
        return None

    # For each trigger onset, find the nearest subsequent signal onset
    lags_s = []
    for t in trig_onsets:
        future = sig_onsets[sig_onsets >= t]
        if len(future) == 0:
            continue
        lag = (future[0] - t) / sfreq
        if lag < 1.0:          # ignore if > 1 s (probably unrelated event)
            lags_s.append(lag)

    lags_s = np.array(lags_s)
    if len(lags_s) == 0:
        print("  ERROR: no paired onsets found within 1 s")
        return None

    counts, bin_edges = np.histogram(lags_s * 1000, bins=30)
    peak_bin_center = (bin_edges[np.argmax(counts)] + bin_edges[np.argmax(counts) + 1]) / 2

    print(f"\n  Lag ({signal_ch} - {trigger_ch}):")
    print(f"    n pairs  = {len(lags_s)}")
    print(f"    mean     = {lags_s.mean()*1000:.2f} ms")
    print(f"    median   = {np.median(lags_s)*1000:.2f} ms")
    print(f"    std      = {lags_s.std()*1000:.2f} ms")
    print(f"    min/max  = {lags_s.min()*1000:.2f} / {lags_s.max()*1000:.2f} ms")
    print(f"    peak bin = {peak_bin_center:.2f} ms  (count={counts.max()})")

    # --- plot ---
    fig, axes = plt.subplots(2, 1, figsize=(14, 6))
    fig.suptitle(label)

    times = raw.times
    axes[0].plot(times, trig_data, label=trigger_ch, alpha=0.8)
    axes[0].plot(times, sig_data,  label=signal_ch,  alpha=0.8)
    axes[0].set_xlabel('Time (s)')
    axes[0].set_ylabel('Amplitude')
    axes[0].legend()
    axes[0].set_title('Full trace (first 2 s)')
    axes[0].set_xlim(0, min(2, times[-1]))

    axes[1].hist(lags_s * 1000, bins=30, edgecolor='k')
    axes[1].set_xlabel('Lag (ms)')
    axes[1].set_ylabel('Count')
    axes[1].set_title(f'Lag distribution  (mean={lags_s.mean()*1000:.1f} ms, '
                      f'std={lags_s.std()*1000:.1f} ms)')
    plt.tight_layout()
    plt.show(block=False)

    return lags_s


# plt.ion()

audio_lags = compute_lag(
    '/Users/matsvanes/Documents/Werk/NTAD/delay/ntad_avtask.fif',
    trigger_ch='STI101',
    signal_ch='MISC012',
    label='Audio lag (MISC012 vs STI101)',
)

photo_lags = compute_lag(
    '/Users/matsvanes/Documents/Werk/NTAD/delay/ntad_scenerep.fif',
    trigger_ch='STI101',
    signal_ch='MISC011',
    label='Photodiode lag (MISC011 vs STI101)',
)

print("\n=== SUMMARY ===")
if audio_lags is not None:
    print(f"  Audio lag    : {np.median(audio_lags)*1000:.2f} ms  (median)")
if photo_lags is not None:
    print(f"  Photodiode lag : {np.median(photo_lags)*1000:.2f} ms  (median)")

# plt.show(block=True)
