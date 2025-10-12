#!/usr/bin/env python3
"""
Test enhanced interestingness scoring on a few files.
"""

import sys
from pathlib import Path
import json
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


def calculate_enhanced_interestingness(result, whistles, signal_clean, fs):
    """
    Calculate enhanced interestingness score with multiple features.

    Features considered:
    1. Whistle count and coverage (basic)
    2. Whistle diversity (frequency and duration variety)
    3. Signal quality (SNR estimation)
    4. Whistle complexity (frequency modulation)
    5. Activity patterns (clustering vs spread)
    """
    score = 0.0
    features = {}

    # === FEATURE 1: Basic Whistle Activity (30 points) ===
    n_whistles = result.get("n_whistles", 0)
    coverage = result.get("whistle_coverage_percent", 0)

    # Whistle count (0-15 pts): Diminishing returns after 30 whistles
    whistle_score = min(15, (n_whistles / 30) * 15)
    score += whistle_score
    features["whistle_count_score"] = round(whistle_score, 2)

    # Coverage (0-15 pts): Percentage of time with whistles
    coverage_score = min(15, coverage * 0.15)
    score += coverage_score
    features["coverage_score"] = round(coverage_score, 2)

    # === FEATURE 2: Whistle Diversity (20 points) ===
    if whistles and len(whistles) >= 2:
        # Frequency diversity
        freqs = [w.get("mean_freq", 0) for w in whistles]
        freq_std = np.std(freqs)
        freq_range = np.max(freqs) - np.min(freqs) if freqs else 0
        freq_diversity = min(10, (freq_range / 10000) * 10)  # 0-10 pts

        # Duration diversity
        durations = [w.get("duration", 0) for w in whistles]
        dur_std = np.std(durations)
        dur_diversity = min(10, dur_std * 20)  # 0-10 pts

        diversity_score = freq_diversity + dur_diversity
        score += diversity_score
        features["diversity_score"] = round(diversity_score, 2)
        features["freq_range_hz"] = round(freq_range, 1)
        features["duration_std"] = round(dur_std, 3)
    else:
        features["diversity_score"] = 0

    # === FEATURE 3: Signal Quality (15 points) ===
    # Estimate SNR by comparing whistle band power to noise floor
    try:
        # Power in whistle band (5-25 kHz)
        whistle_band = signal_clean[::10]  # Downsample for speed
        fft = np.fft.rfft(whistle_band)
        power_spectrum = np.abs(fft) ** 2

        # Simplified SNR estimate
        freq_bins = np.fft.rfftfreq(len(whistle_band), 1 / fs)
        whistle_mask = (freq_bins >= 5000) & (freq_bins <= 25000)
        noise_mask = (freq_bins >= 1000) & (freq_bins <= 5000)

        if np.any(whistle_mask) and np.any(noise_mask):
            signal_power = np.mean(power_spectrum[whistle_mask])
            noise_power = np.mean(power_spectrum[noise_mask])
            snr = 10 * np.log10(signal_power / (noise_power + 1e-10))

            # 0-15 pts based on SNR (typically 0-30 dB)
            snr_score = min(15, max(0, (snr / 30) * 15))
            score += snr_score
            features["snr_db"] = round(snr, 1)
            features["snr_score"] = round(snr_score, 2)
        else:
            features["snr_score"] = 0
    except:
        features["snr_score"] = 0

    # === FEATURE 4: Whistle Complexity (15 points) ===
    if whistles and len(whistles) > 0:
        # Look for frequency modulation (FM) complexity
        fm_scores = []
        for w in whistles[:10]:  # Check up to 10 whistles
            if "frequency" in w and len(w["frequency"]) > 3:
                freqs = w["frequency"]
                # Measure frequency variation (FM rate)
                freq_diff = np.abs(np.diff(freqs))
                fm_rate = np.mean(freq_diff) if len(freq_diff) > 0 else 0
                fm_scores.append(fm_rate)

        if fm_scores:
            mean_fm = np.mean(fm_scores)
            # 0-15 pts: More modulation = more complex = more interesting
            complexity_score = min(15, (mean_fm / 500) * 15)  # 500 Hz typical FM
            score += complexity_score
            features["complexity_score"] = round(complexity_score, 2)
            features["mean_fm_rate"] = round(mean_fm, 1)
        else:
            features["complexity_score"] = 0
    else:
        features["complexity_score"] = 0

    # === FEATURE 5: Activity Patterns (20 points) ===
    if whistles and len(whistles) >= 3:
        # Check temporal distribution
        start_times = np.array([w["start_time"] for w in whistles])

        # Clustering: Are whistles in bursts or evenly spread?
        gaps = np.diff(sorted(start_times))
        if len(gaps) > 0:
            gap_std = np.std(gaps)
            mean_gap = np.mean(gaps)

            # Bursting pattern (low gap variance) = interesting
            burst_score = min(10, (1.0 / (gap_std + 0.01)) * 2)

            # Sustained activity (short gaps) = interesting
            sustained_score = min(10, max(0, (1.0 - mean_gap) * 10))

            pattern_score = burst_score + sustained_score
            score += pattern_score
            features["pattern_score"] = round(pattern_score, 2)
            features["mean_gap_s"] = round(mean_gap, 2)
        else:
            features["pattern_score"] = 0
    else:
        features["pattern_score"] = 0

    # === BONUS: Multi-whistle overlaps (up to 10 points) ===
    if whistles and len(whistles) >= 2:
        # Check for simultaneous whistles (possible multiple dolphins)
        overlaps = 0
        for i, w1 in enumerate(whistles[:-1]):
            for w2 in whistles[i + 1 :]:
                if (
                    w1["start_time"] <= w2["end_time"]
                    and w2["start_time"] <= w1["end_time"]
                ):
                    overlaps += 1

        overlap_score = min(10, overlaps * 2)
        score += overlap_score
        features["overlap_bonus"] = round(overlap_score, 2)
        features["n_overlaps"] = overlaps
    else:
        features["overlap_bonus"] = 0

    features["total_score"] = round(score, 2)
    return score, features


def test_enhanced_scoring():
    """Test on a few files to see the difference."""
    print("=" * 80)
    print("🧪 TESTING ENHANCED INTERESTINGNESS SCORING")
    print("=" * 80)
    print()

    # Load some files from checkpoint
    checkpoint = Path("outputs/results/large_run/checkpoint.json")
    if not checkpoint.exists():
        checkpoint = Path("quick_find_results/checkpoint.json")

    with open(checkpoint) as f:
        data = json.load(f)

    results = data["results"][:10]  # Test on first 10

    print(f"Testing on {len(results)} files...")
    print()

    comparisons = []

    for result in results:
        file_path = Path(result["file"])
        if not file_path.exists():
            continue

        print(f"Processing: {file_path.name}")

        # Read and process
        data_dict = dolphain.read_ears_file(file_path)
        signal_clean = dolphain.wavelet_denoise(data_dict["data"])
        whistles = dolphain.detect_whistles(signal_clean, data_dict["fs"])

        # Calculate old score
        old_score = result.get("interestingness_score", 0)

        # Calculate new score
        new_score, features = calculate_enhanced_interestingness(
            result, whistles, signal_clean, data_dict["fs"]
        )

        print(f"  Old score: {old_score:.1f}")
        print(f"  New score: {new_score:.1f}")
        print(f"  Features: {features}")
        print()

        comparisons.append(
            {
                "filename": file_path.name,
                "old_score": old_score,
                "new_score": new_score,
                "features": features,
            }
        )

    # Summary
    print("=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)

    # Sort by new score
    comparisons.sort(key=lambda x: x["new_score"], reverse=True)

    print("\nTOP 5 by NEW scoring:")
    for i, c in enumerate(comparisons[:5], 1):
        print(f"{i}. {c['filename']}")
        print(f"   Old: {c['old_score']:.1f} → New: {c['new_score']:.1f}")

    print("\nTOP 5 by OLD scoring:")
    old_sorted = sorted(comparisons, key=lambda x: x["old_score"], reverse=True)
    for i, c in enumerate(old_sorted[:5], 1):
        print(f"{i}. {c['filename']}")
        print(f"   Old: {c['old_score']:.1f} → New: {c['new_score']:.1f}")

    print("\n✅ Test complete!")


if __name__ == "__main__":
    test_enhanced_scoring()
