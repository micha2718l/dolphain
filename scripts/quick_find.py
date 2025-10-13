#!/usr/bin/env python3
"""
Quick-start script for finding interesting files with chirps and click trains.

This version focuses on detecting:
1. Chirp signals - frequency sweeps visible in spectrograms (from various sources)
2. Click trains - rapid high-frequency clicks from dolphins

Usage:
    python quick_find.py --file-list ears_files_list.txt --n-files 100

    # Resume if interrupted
    python quick_find.py --file-list ears_files_list.txt --n-files 1000 --resume
"""

import sys
import argparse
from pathlib import Path
import time
import numpy as np
from scipy import signal as sp_signal
from scipy.ndimage import maximum_filter

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


def detect_chirps(data, fs, min_duration=0.3, freq_sweep_min=3000):
    """
    Detect chirp signals (frequency sweeps) in acoustic data.

    Chirps are characterized by STRONG continuous frequency sweeps that appear as
    clear diagonal lines in the spectrogram. This is a conservative detector.

    Parameters
    ----------
    data : array_like
        Input acoustic data
    fs : int
        Sampling frequency in Hz
    min_duration : float
        Minimum chirp duration in seconds (default: 0.3s - longer = more selective)
    freq_sweep_min : float
        Minimum frequency sweep range in Hz (default: 3000 Hz - must sweep significantly)

    Returns
    -------
    chirps : list of dict
        List of detected chirps with time, frequency, and sweep information
    """
    data = np.asarray(data)

    # Use large FFT for good frequency resolution
    nperseg = 8192  # Larger for better frequency resolution
    noverlap = int(0.5 * nperseg)

    # Compute spectrogram
    f, t, Sxx = sp_signal.spectrogram(
        data,
        fs=fs,
        nperseg=nperseg,
        noverlap=noverlap,
        window="hann",
        scaling="density",
    )

    # Convert to dB
    Sxx_dB = 10 * np.log10(Sxx + 1e-12)

    # Very high threshold - only the strongest signals (95th percentile)
    power_threshold = np.percentile(Sxx_dB, 95)

    # Additional absolute threshold - must be significantly above noise floor
    noise_floor = np.percentile(Sxx_dB, 10)
    min_snr_db = 15  # Must be 15 dB above noise floor
    absolute_threshold = noise_floor + min_snr_db
    power_threshold = max(power_threshold, absolute_threshold)

    chirps = []

    for time_idx in range(len(t)):
        col = Sxx_dB[:, time_idx]

        # Find strong local maxima only
        local_max_mask = col > power_threshold

        # Require strict local maximum (higher than neighbors in time)
        if time_idx > 0:
            local_max_mask &= col > Sxx_dB[:, time_idx - 1]
        if time_idx < len(t) - 1:
            local_max_mask &= col > Sxx_dB[:, time_idx + 1]

        # Require strict local maximum in frequency (higher than neighbors)
        for i in range(1, len(col) - 1):
            if local_max_mask[i]:
                if col[i] <= col[i - 1] or col[i] <= col[i + 1]:
                    local_max_mask[i] = False

        peak_freqs = np.where(local_max_mask)[0]

        # Try to extend existing chirps
        extended = set()
        for chirp in chirps:
            if chirp["end_time_idx"] == time_idx - 1:  # Adjacent in time
                last_freq = chirp["freq_indices"][-1]
                if len(peak_freqs) > 0:
                    closest = peak_freqs[np.argmin(np.abs(peak_freqs - last_freq))]
                    freq_diff = abs(closest - last_freq)
                    # Stricter continuation - must be close or continuing sweep
                    if freq_diff < 8:  # Tighter tolerance
                        chirp["time_indices"].append(time_idx)
                        chirp["freq_indices"].append(closest)
                        chirp["end_time_idx"] = time_idx
                        extended.add(closest)

        # Start new chirps - only from top 3 strongest peaks (very conservative)
        unused_peaks = [p for p in peak_freqs if p not in extended]
        if len(unused_peaks) > 3:
            peak_powers = [col[p] for p in unused_peaks]
            top_3_idx = np.argsort(peak_powers)[-3:]
            unused_peaks = [unused_peaks[i] for i in top_3_idx]

        for peak in unused_peaks:
            chirps.append(
                {
                    "time_indices": [time_idx],
                    "freq_indices": [peak],
                    "end_time_idx": time_idx,
                }
            )

    # Very strict filtering - only clear, strong sweeps
    result_chirps = []
    min_time_points = int(min_duration * fs / nperseg)
    freq_bin_width = fs / nperseg
    min_freq_bins = freq_sweep_min / freq_bin_width

    for chirp in chirps:
        # Must be long enough
        if len(chirp["time_indices"]) < min_time_points:
            continue

        time_indices = np.array(chirp["time_indices"])
        freq_indices = np.array(chirp["freq_indices"])

        # Check frequency sweep - must be substantial
        freq_sweep_bins = abs(freq_indices[-1] - freq_indices[0])
        if freq_sweep_bins < min_freq_bins:
            continue

        # Additional quality check: sweep must be relatively continuous
        # Check that it's actually sweeping, not jumping around
        freq_changes = np.abs(np.diff(freq_indices))
        mean_change = np.mean(freq_changes)
        std_change = np.std(freq_changes)

        # Reject if too erratic (jumping around vs smooth sweep)
        if std_change > 3 * mean_change:
            continue

        times = t[time_indices]
        freqs = f[freq_indices]

        duration = times[-1] - times[0]
        freq_sweep = abs(freqs[-1] - freqs[0])

        result_chirps.append(
            {
                "start_time": times[0],
                "end_time": times[-1],
                "duration": duration,
                "start_freq": freqs[0],
                "end_freq": freqs[-1],
                "freq_sweep": freq_sweep,
                "sweep_rate": freq_sweep / duration if duration > 0 else 0,
                "min_freq": freqs.min(),
                "max_freq": freqs.max(),
                "n_points": len(times),
            }
        )

    return result_chirps


def detect_click_trains(
    data, fs, click_freq_range=(20000, 150000), min_clicks=10, max_ici=0.05
):
    """
    Detect dolphin click trains in acoustic data.

    Click trains are sequences of rapid, broadband, HIGH-AMPLITUDE clicks
    used by dolphins for echolocation. This is a conservative detector.

    Parameters
    ----------
    data : array_like
        Input acoustic data
    fs : int
        Sampling frequency in Hz
    click_freq_range : tuple
        Frequency range for click detection in Hz (default: 20-150 kHz)
    min_clicks : int
        Minimum number of clicks to constitute a train (default: 10, very selective)
    max_ici : float
        Maximum inter-click interval in seconds (default: 0.05s = 50ms)

    Returns
    -------
    click_trains : list of dict
        List of detected click trains with timing and rate information
    """
    data = np.asarray(data)

    # Band-pass filter to click frequency range (higher frequency for true clicks)
    nyquist = fs / 2.0
    low = max(click_freq_range[0] / nyquist, 0.001)
    high = min(click_freq_range[1] / nyquist, 0.999)

    if high <= low:
        return []

    # Higher order filter for sharper cutoff
    sos = sp_signal.butter(6, [low, high], btype="bandpass", output="sos")
    filtered = sp_signal.sosfiltfilt(sos, data)

    # Compute envelope using Hilbert transform
    analytic = sp_signal.hilbert(filtered)
    envelope = np.abs(analytic)

    # Minimal smoothing to preserve sharp click edges
    kernel_size = int(fs * 0.0005)  # 0.5ms (was 1ms)
    if kernel_size % 2 == 0:
        kernel_size += 1
    if kernel_size >= 3:
        envelope = sp_signal.medfilt(envelope, kernel_size=kernel_size)

    # Much higher threshold - only very strong clicks (99th percentile!)
    threshold_percentile = np.percentile(envelope, 99)

    # Also require absolute threshold well above noise
    noise_level = np.percentile(envelope, 20)
    min_click_amplitude = noise_level * 8  # Must be 8x noise level (was 5x)
    threshold = max(threshold_percentile, min_click_amplitude)

    # Find peaks with stricter criteria
    min_separation = int(fs * 0.002)  # At least 2ms between clicks (was 1ms)

    # Require sharp, prominent peaks
    peak_indices, properties = sp_signal.find_peaks(
        envelope,
        height=threshold,
        distance=min_separation,
        prominence=threshold * 0.3,  # Must be prominent (30% of threshold)
        width=(
            1,
            int(fs * 0.005),
        ),  # Width between 1 sample and 5ms (reject wide bumps)
    )

    if len(peak_indices) < min_clicks:
        return []

    # Additional quality filter: check peak sharpness
    sharp_peaks = []
    for idx in peak_indices:
        # Check that peak is sharp (high amplitude, narrow width)
        start = max(0, idx - int(fs * 0.002))
        end = min(len(envelope), idx + int(fs * 0.002))
        local_region = envelope[start:end]
        peak_val = envelope[idx]

        # Require peak to dominate local region
        if peak_val > np.percentile(local_region, 90):
            sharp_peaks.append(idx)

    if len(sharp_peaks) < min_clicks:
        return []

    peak_indices = np.array(sharp_peaks)
    peak_times = peak_indices / fs

    # Group peaks into click trains based on ICI
    click_trains = []
    current_train = [peak_times[0]]

    for i in range(1, len(peak_times)):
        ici = peak_times[i] - peak_times[i - 1]

        if ici <= max_ici:
            # Continue current train
            current_train.append(peak_times[i])
        else:
            # Save current train if long enough
            if len(current_train) >= min_clicks:
                train_data = np.array(current_train)
                icis = np.diff(train_data)

                click_trains.append(
                    {
                        "start_time": train_data[0],
                        "end_time": train_data[-1],
                        "duration": train_data[-1] - train_data[0],
                        "n_clicks": len(train_data),
                        "mean_ici": np.mean(icis),
                        "std_ici": np.std(icis),
                        "click_rate": (
                            len(train_data) / (train_data[-1] - train_data[0])
                            if train_data[-1] > train_data[0]
                            else 0
                        ),
                        "click_times": train_data.tolist(),
                    }
                )

            # Start new train
            current_train = [peak_times[i]]

    # Don't forget the last train
    if len(current_train) >= min_clicks:
        train_data = np.array(current_train)
        icis = np.diff(train_data)

        click_trains.append(
            {
                "start_time": train_data[0],
                "end_time": train_data[-1],
                "duration": train_data[-1] - train_data[0],
                "n_clicks": len(train_data),
                "mean_ici": np.mean(icis),
                "std_ici": np.std(icis),
                "click_rate": (
                    len(train_data) / (train_data[-1] - train_data[0])
                    if train_data[-1] > train_data[0]
                    else 0
                ),
                "click_times": train_data.tolist(),
            }
        )

    return click_trains


def calculate_interestingness_score(result, chirps, click_trains, signal_clean, fs):
    """
    Calculate interestingness score based on chirps and click trains.

    Scoring (0-100):
    - Chirp activity: 40 points (quantity, sweep quality, diversity)
    - Click train activity: 40 points (quantity, regularity, rate)
    - Signal quality: 20 points (SNR, clarity)
    """
    score = 0.0

    n_chirps = result.get("n_chirps", 0)
    n_click_trains = result.get("n_click_trains", 0)
    total_clicks = result.get("total_clicks", 0)

    # === CHIRP SCORING (40 points) ===

    # Basic chirp count (15 points)
    score += min(15, (n_chirps / 20) * 15)

    # Chirp quality - sweep range and rate (15 points)
    if chirps and len(chirps) > 0:
        sweep_ranges = [c["freq_sweep"] for c in chirps]
        sweep_rates = [c["sweep_rate"] for c in chirps]

        mean_sweep = np.mean(sweep_ranges)
        mean_rate = np.mean(sweep_rates)

        # Reward large frequency sweeps (up to 10 points)
        score += min(10, (mean_sweep / 5000) * 10)

        # Reward fast sweeps (up to 5 points)
        score += min(5, (mean_rate / 2000) * 5)

    # Chirp diversity - variety in frequencies (10 points)
    if chirps and len(chirps) >= 2:
        start_freqs = [c["start_freq"] for c in chirps]
        freq_std = np.std(start_freqs)
        score += min(10, (freq_std / 5000) * 10)

    # === CLICK TRAIN SCORING (40 points) ===

    # Click train count (10 points)
    score += min(10, (n_click_trains / 10) * 10)

    # Total clicks (10 points)
    score += min(10, (total_clicks / 100) * 10)

    # Click train regularity (10 points)
    if click_trains and len(click_trains) > 0:
        # Reward consistent ICIs (lower std = more regular)
        ici_stds = [ct["std_ici"] for ct in click_trains]
        mean_ici_std = np.mean(ici_stds)
        regularity = max(0, 1.0 - (mean_ici_std / 0.02))  # Normalize by 20ms
        score += regularity * 10

    # Click rate quality (10 points)
    if click_trains and len(click_trains) > 0:
        click_rates = [ct["click_rate"] for ct in click_trains]
        mean_rate = np.mean(click_rates)
        # Typical dolphin click rates: 20-200 clicks/sec
        if 20 <= mean_rate <= 200:
            score += 10
        elif mean_rate < 20:
            score += (mean_rate / 20) * 10
        else:
            score += max(0, 10 - ((mean_rate - 200) / 100))

    # === SIGNAL QUALITY (20 points) ===

    # Compute SNR in relevant frequency bands
    try:
        # Downsample for faster FFT
        signal_ds = signal_clean[::10]
        fft = np.fft.rfft(signal_ds)
        power_spectrum = np.abs(fft) ** 2
        freq_bins = np.fft.rfftfreq(len(signal_ds), 10 / fs)

        # High-frequency signal band (clicks + chirps)
        signal_mask = (freq_bins >= 5000) & (freq_bins <= 50000)
        noise_mask = (freq_bins >= 500) & (freq_bins <= 2000)

        if np.any(signal_mask) and np.any(noise_mask):
            signal_power = np.mean(power_spectrum[signal_mask])
            noise_power = np.mean(power_spectrum[noise_mask])
            snr = 10 * np.log10(signal_power / (noise_power + 1e-10))
            score += min(20, max(0, (snr / 30) * 20))
    except:
        pass

    return score


def quick_find(
    data_dir: Path = None,
    file_list_path: Path = None,
    n_files: int = 1000,
    output_dir: Path = None,
    resume: bool = False,
):
    """
    Quick analysis to find files with interesting chirps and click trains.

    Args:
        data_dir: Root directory to search (deprecated, use file_list_path)
        file_list_path: Path to pre-generated file list (one file per line)
        n_files: Number of files to sample
        output_dir: Where to save results
        resume: Resume from checkpoint if interrupted
    """
    output_dir = output_dir or Path("quick_find_results")
    output_dir.mkdir(exist_ok=True)
    checkpoint_file = output_dir / "checkpoint.json"

    print("=" * 80)
    print("🐬 QUICK FIND - CHIRPS & CLICK TRAINS")
    print("=" * 80)
    print(f"Sample size: {n_files} files")
    print(f"Output: {output_dir}")
    print(f"Detection targets:")
    print(f"  🎵 Chirps: Frequency sweeps (from various sources)")
    print(f"  🔊 Click trains: Rapid high-frequency clicks (dolphin echolocation)")
    if resume and checkpoint_file.exists():
        print("📂 Resume mode: Will continue from checkpoint")
    print()

    # Step 1: Load file list
    print("📋 Step 1: Loading EARS file list...")
    start_time = time.time()

    if file_list_path and file_list_path.exists():
        print(f"  Reading from: {file_list_path}")
        with open(file_list_path, "r") as f:
            all_files = [Path(line.strip()) for line in f if line.strip()]
        print(f"  Loaded {len(all_files)} files from list")
    elif data_dir:
        print(f"  Scanning directory: {data_dir}")
        all_files = dolphain.find_data_files(data_dir, "**/*.[0-9][0-9][0-9]")
        print(f"  Found {len(all_files)} total EARS files")
    else:
        print("  ❌ Must provide either --file-list or --data-dir")
        return

    if len(all_files) == 0:
        print("  ❌ No EARS files found!")
        return

    # Sample if needed
    if len(all_files) > n_files:
        import random

        file_list = random.sample(all_files, n_files)
        print(f"  Sampling {n_files} files randomly")
    else:
        file_list = all_files
        print(f"  Using all {len(file_list)} files")

    print(f"  Time: {time.time() - start_time:.1f}s\n")

    # Check for checkpoint
    processed_files = set()
    results = []
    errors = []

    if resume and checkpoint_file.exists():
        print("📂 Loading checkpoint...")
        import json

        with open(checkpoint_file, "r") as f:
            checkpoint = json.load(f)
        results = checkpoint.get("results", [])
        errors = checkpoint.get("errors", [])
        processed_files = set(r["file"] for r in results)
        processed_files.update(e["file"] for e in errors)
        print(f"  ✓ Loaded {len(results)} completed files")
        print(f"  ✓ Resuming from file {len(processed_files) + 1}/{len(file_list)}\n")

    # Step 2: Analysis
    print("🔍 Step 2: Detecting chirps and click trains...")
    print(f"  Will save checkpoint every 10 files (safe to interrupt!)")
    start_time = time.time()

    files_to_process = [f for f in file_list if str(f) not in processed_files]
    total_files = len(file_list)
    already_done = len(processed_files)

    print(f"  📊 Status: {already_done}/{total_files} files already processed")
    print(f"  🚀 Processing {len(files_to_process)} remaining files...\n")

    for i, file_path in enumerate(files_to_process):
        overall_index = already_done + i
        try:
            # Read and process file
            data_dict = dolphain.read_ears_file(file_path)
            # More aggressive denoising to remove noise before detection
            signal_clean = dolphain.wavelet_denoise(
                data_dict["data"],
                wavelet="db8",
                hard_threshold=True,  # More aggressive: hard thresholding removes more noise
            )

            # Detect chirps (very conservative parameters)
            chirps = detect_chirps(
                signal_clean,
                data_dict["fs"],
                min_duration=0.3,  # Longer minimum duration
                freq_sweep_min=3000,  # Larger frequency sweep required
            )

            # Detect click trains (very conservative)
            click_trains = detect_click_trains(
                signal_clean,
                data_dict["fs"],
                click_freq_range=(
                    20000,
                    min(data_dict["fs"] // 2, 150000),
                ),  # Higher frequency minimum
                min_clicks=10,  # More clicks required (was 8)
                max_ici=0.05,
            )

            # Calculate statistics
            n_chirps = len(chirps)
            n_click_trains = len(click_trains)
            total_clicks = sum(ct["n_clicks"] for ct in click_trains)

            # Coverage calculations
            if n_chirps > 0:
                chirp_duration = sum(c["duration"] for c in chirps)
                chirp_coverage = chirp_duration / data_dict["duration"] * 100
                mean_chirp_duration = chirp_duration / n_chirps
                mean_sweep = np.mean([c["freq_sweep"] for c in chirps])
            else:
                chirp_coverage = 0.0
                mean_chirp_duration = 0.0
                mean_sweep = 0.0

            if n_click_trains > 0:
                ct_duration = sum(ct["duration"] for ct in click_trains)
                ct_coverage = ct_duration / data_dict["duration"] * 100
                mean_ct_duration = ct_duration / n_click_trains
                mean_click_rate = np.mean([ct["click_rate"] for ct in click_trains])
                mean_ici = np.mean([ct["mean_ici"] for ct in click_trains])
            else:
                ct_coverage = 0.0
                mean_ct_duration = 0.0
                mean_click_rate = 0.0
                mean_ici = 0.0

            result = {
                "file": str(file_path),
                "filename": file_path.name,
                "recording_duration": data_dict["duration"],
                # Chirp data
                "n_chirps": n_chirps,
                "chirp_coverage_percent": chirp_coverage,
                "mean_chirp_duration": mean_chirp_duration,
                "mean_freq_sweep": mean_sweep,
                # Click train data
                "n_click_trains": n_click_trains,
                "total_clicks": total_clicks,
                "click_train_coverage_percent": ct_coverage,
                "mean_click_train_duration": mean_ct_duration,
                "mean_click_rate": mean_click_rate,
                "mean_ici": mean_ici,
            }

            # Calculate interestingness score
            score = calculate_interestingness_score(
                result, chirps, click_trains, signal_clean, data_dict["fs"]
            )
            result["interestingness_score"] = round(score, 2)
            results.append(result)

        except Exception as e:
            errors.append({"file": str(file_path), "error": str(e)})

        # Save checkpoint every 10 files
        if (overall_index + 1) % 10 == 0:
            import json

            with open(checkpoint_file, "w") as f:
                json.dump(
                    {"results": results, "errors": errors, "last_updated": time.time()},
                    f,
                    indent=2,
                )

        # Progress updates every 10 files
        if (overall_index + 1) % 10 == 0 or (overall_index + 1) == total_files:
            elapsed = time.time() - start_time
            files_done = overall_index + 1 - already_done
            if files_done > 0:
                rate = files_done / elapsed
                remaining_files = total_files - overall_index - 1
                remaining_time = remaining_files / rate if rate > 0 else 0

                # Calculate stats so far
                n_with_chirps = sum(1 for r in results if r.get("n_chirps", 0) > 0)
                n_with_clicks = sum(
                    1 for r in results if r.get("n_click_trains", 0) > 0
                )
                n_with_both = sum(
                    1
                    for r in results
                    if r.get("n_chirps", 0) > 0 and r.get("n_click_trains", 0) > 0
                )

                chirp_rate = (n_with_chirps / len(results) * 100) if results else 0
                click_rate = (n_with_clicks / len(results) * 100) if results else 0

                print(
                    f"  ⏳ Progress: {overall_index + 1}/{total_files} ({(overall_index + 1)/total_files*100:.1f}%) "
                    f"| {rate:.1f} files/s | ETA: {remaining_time/60:.1f}m"
                )
                print(
                    f"     Chirps: {chirp_rate:.0f}% | Clicks: {click_rate:.0f}% | Both: {n_with_both} | Checkpoint saved ✓"
                )

    # Clean up checkpoint on completion
    if checkpoint_file.exists():
        checkpoint_file.unlink()

    print(f"\n  ✅ Completed {len(results)} files successfully")
    print(f"  Errors: {len(errors)}")
    print(f"  Time: {time.time() - start_time:.1f}s\n")

    # Step 3: Analyze and report
    print("📊 Step 3: Generating report...")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sort by interestingness
    results.sort(key=lambda x: x["interestingness_score"], reverse=True)

    # Save full results
    import json

    with open(output_dir / "results.json", "w") as f:
        json.dump(
            {
                "n_analyzed": len(results),
                "n_errors": len(errors),
                "detection_targets": ["chirps", "click_trains"],
                "results": results,
                "errors": errors,
            },
            f,
            indent=2,
        )

    # Save top files list
    top_20 = results[:20]
    with open(output_dir / "top_20_files.txt", "w") as f:
        f.write("TOP 20 MOST INTERESTING FILES - CHIRPS & CLICK TRAINS\n")
        f.write("=" * 100 + "\n\n")
        f.write(
            f"{'Rank':<6} {'Score':<8} {'Chirps':<8} {'Clicks':<8} {'CT':<6} {'File'}\n"
        )
        f.write("-" * 100 + "\n")

        for i, result in enumerate(top_20, 1):
            score = result["interestingness_score"]
            chirps = result.get("n_chirps", 0)
            clicks = result.get("total_clicks", 0)
            ct = result.get("n_click_trains", 0)
            filename = result["filename"]

            f.write(
                f"{i:<6} {score:<8.1f} {chirps:<8} {clicks:<8} {ct:<6} {filename}\n"
            )

        f.write("\n\nFull file paths:\n")
        f.write("-" * 100 + "\n")
        for i, result in enumerate(top_20, 1):
            f.write(f"{i}. {result['file']}\n")

    # Save CSV for analysis
    import pandas as pd

    df = pd.DataFrame(results)
    df.to_csv(output_dir / "all_results.csv", index=False)

    print(f"  ✓ Saved: {output_dir}/results.json")
    print(f"  ✓ Saved: {output_dir}/top_20_files.txt")
    print(f"  ✓ Saved: {output_dir}/all_results.csv")

    # Print summary
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"Files analyzed: {len(results)}")

    n_with_chirps = sum(1 for r in results if r.get("n_chirps", 0) > 0)
    n_with_clicks = sum(1 for r in results if r.get("n_click_trains", 0) > 0)
    n_with_both = sum(
        1
        for r in results
        if r.get("n_chirps", 0) > 0 and r.get("n_click_trains", 0) > 0
    )

    print(f"Files with chirps: {n_with_chirps} ({n_with_chirps/len(results)*100:.1f}%)")
    print(
        f"Files with click trains: {n_with_clicks} ({n_with_clicks/len(results)*100:.1f}%)"
    )
    print(f"Files with both: {n_with_both} ({n_with_both/len(results)*100:.1f}%)")

    total_chirps = sum(r.get("n_chirps", 0) for r in results)
    total_click_trains = sum(r.get("n_click_trains", 0) for r in results)
    total_clicks = sum(r.get("total_clicks", 0) for r in results)

    print(f"Total chirps detected: {total_chirps}")
    print(f"Total click trains detected: {total_click_trains}")
    print(f"Total clicks detected: {total_clicks}")
    print()

    print("TOP 5 FILES:")
    for i, result in enumerate(results[:5], 1):
        score = result["interestingness_score"]
        chirps = result.get("n_chirps", 0)
        clicks = result.get("total_clicks", 0)
        ct = result.get("n_click_trains", 0)
        print(
            f"  {i}. Score: {score:.1f} | Chirps: {chirps} | Click trains: {ct} ({clicks} clicks)"
        )
        print(f"     {result['filename']}")

    print("\n" + "=" * 80)
    print("✅ QUICK FIND COMPLETE!")
    print("=" * 80)
    print(f"\nResults saved to: {output_dir}/")
    print(f"\nNext steps:")
    print(f"  1. Review top_20_files.txt")
    print(f"  2. Copy interesting files to working directory")
    print(f"  3. Visualize: python scripts/ears_to_wav.py <file> --plot")


def main():
    parser = argparse.ArgumentParser(
        description="Quick find EARS files with chirps and click trains",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use pre-generated file list (RECOMMENDED - much faster!)
  python quick_find.py --file-list ears_files_list.txt --n-files 100
  
  # Resume if interrupted (safe to Ctrl+C anytime!)
  python quick_find.py --file-list ears_files_list.txt --n-files 1000 --resume
  
  # Scan directory (slow on external drives)
  python quick_find.py --data-dir /Volumes/ladcuno8tb0/ --n-files 500
  
  # Custom output location
  python quick_find.py --file-list ears_files_list.txt --output-dir my_results/

Detection:
  🎵 Chirps: Frequency sweeps seen in spectrograms
  🔊 Click trains: Rapid high-frequency clicks from dolphins

Note: Checkpoints are saved every 10 files, so you can safely interrupt (Ctrl+C) 
      and resume later with --resume flag!
        """,
    )

    parser.add_argument(
        "--data-dir", type=Path, help="Root directory containing EARS files (slow)"
    )
    parser.add_argument(
        "--file-list",
        type=Path,
        help="Pre-generated file list (one file per line) - RECOMMENDED",
    )
    parser.add_argument(
        "--n-files",
        type=int,
        default=1000,
        help="Number of files to sample (default: 1000)",
    )
    parser.add_argument(
        "--output-dir", type=Path, help="Output directory (default: quick_find_results)"
    )
    parser.add_argument(
        "--resume", action="store_true", help="Resume from checkpoint if interrupted"
    )

    args = parser.parse_args()

    # Validate
    if not args.file_list and not args.data_dir:
        print("❌ Error: Must provide either --file-list or --data-dir")
        parser.print_help()
        sys.exit(1)

    if args.data_dir and not args.data_dir.exists():
        print(f"❌ Error: Directory not found: {args.data_dir}")
        print(f"   Is the drive mounted?")
        sys.exit(1)

    if args.file_list and not args.file_list.exists():
        print(f"❌ Error: File list not found: {args.file_list}")
        print(f"   Run: python scripts/crawl_data_drive.py first")
        sys.exit(1)

    # Run
    quick_find(
        data_dir=args.data_dir,
        file_list_path=args.file_list,
        n_files=args.n_files,
        output_dir=args.output_dir,
        resume=args.resume,
    )


if __name__ == "__main__":
    main()
