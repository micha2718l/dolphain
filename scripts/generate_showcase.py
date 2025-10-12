#!/usr/bin/env python3
"""
Generate interactive showcase of top dolphin acoustic files.

Creates:
- Audio files (WAV format for web playback)
- Visualizations (spectrograms, waveforms)
- Statistics and metadata
- JSON data for web page
"""

import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from scipy import signal as scipy_signal
from scipy.io import wavfile
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dolphain.io import read_ears_file
from dolphain.signal import wavelet_denoise, detect_whistles


def create_spectrogram_image(audio_data, sample_rate, output_path, title=""):
    """Create a beautiful spectrogram image."""
    fig, ax = plt.subplots(figsize=(12, 4), facecolor="#0a0e27")
    ax.set_facecolor("#0a0e27")

    # Compute spectrogram
    f, t, Sxx = scipy_signal.spectrogram(
        audio_data, fs=sample_rate, nperseg=512, noverlap=480, window="hann"
    )

    # Plot with nice colormap
    im = ax.pcolormesh(
        t,
        f / 1000,
        10 * np.log10(Sxx + 1e-10),
        shading="gouraud",
        cmap="viridis",
        vmin=-80,
        vmax=-20,
    )

    ax.set_ylabel("Frequency (kHz)", color="white", fontsize=12)
    ax.set_xlabel("Time (seconds)", color="white", fontsize=12)
    ax.set_ylim([0, 50])
    ax.tick_params(colors="white")

    if title:
        ax.set_title(title, color="white", fontsize=14, pad=10)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Power (dB)", color="white", fontsize=10)
    cbar.ax.tick_params(colors="white")

    plt.tight_layout()
    plt.savefig(output_path, dpi=100, facecolor="#0a0e27", edgecolor="none")
    plt.close()


def create_waveform_with_whistles(audio_data, sample_rate, whistles, output_path):
    """Create waveform visualization with whistle overlays."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), facecolor="#0a0e27")

    # Waveform
    ax1.set_facecolor("#0a0e27")
    time = np.arange(len(audio_data)) / sample_rate
    ax1.plot(time, audio_data, color="#00d4ff", linewidth=0.5, alpha=0.8)
    ax1.set_ylabel("Amplitude", color="white", fontsize=10)
    ax1.set_xlim([0, time[-1]])
    ax1.tick_params(colors="white")
    ax1.set_title("Waveform with Detected Whistles", color="white", fontsize=12)

    # Highlight whistle regions
    for w in whistles:
        ax1.axvspan(w["start_time"], w["end_time"], alpha=0.2, color="yellow")

    # Whistle frequency timeline
    ax2.set_facecolor("#0a0e27")
    for w in whistles:
        mid_time = (w["start_time"] + w["end_time"]) / 2
        ax2.scatter(
            mid_time,
            w["mean_freq"] / 1000,
            s=100,
            c="#ff00ff",
            alpha=0.7,
            edgecolors="white",
            linewidth=0.5,
        )
        ax2.plot(
            [w["start_time"], w["end_time"]],
            [w["min_freq"] / 1000, w["max_freq"] / 1000],
            color="#ff00ff",
            alpha=0.5,
            linewidth=2,
        )

    ax2.set_ylabel("Frequency (kHz)", color="white", fontsize=10)
    ax2.set_xlabel("Time (seconds)", color="white", fontsize=10)
    ax2.set_xlim([0, time[-1]])
    ax2.set_ylim([0, 50])
    ax2.tick_params(colors="white")
    ax2.grid(True, alpha=0.2, color="white")

    plt.tight_layout()
    plt.savefig(output_path, dpi=100, facecolor="#0a0e27", edgecolor="none")
    plt.close()


def calculate_statistics(whistles, audio_data, sample_rate):
    """Calculate comprehensive statistics."""
    if not whistles:
        return {
            "whistle_count": 0,
            "duration": len(audio_data) / sample_rate,
            "coverage": 0.0,
        }

    # Basic stats
    duration = len(audio_data) / sample_rate
    whistle_time = sum(w["end_time"] - w["start_time"] for w in whistles)
    coverage = (whistle_time / duration) * 100

    # Frequency stats
    freq_min = min(w["min_freq"] for w in whistles) / 1000
    freq_max = max(w["max_freq"] for w in whistles) / 1000
    freq_mean = np.mean([w["mean_freq"] for w in whistles]) / 1000
    freq_range = freq_max - freq_min

    # Duration stats
    durations = [w["duration"] for w in whistles]
    duration_mean = np.mean(durations)
    duration_std = np.std(durations)

    # Temporal stats
    if len(whistles) > 1:
        gaps = [
            whistles[i + 1]["start_time"] - whistles[i]["end_time"]
            for i in range(len(whistles) - 1)
        ]
        mean_gap = np.mean(gaps)
        gap_std = np.std(gaps)
    else:
        mean_gap = 0
        gap_std = 0

    # Check for overlaps
    overlaps = 0
    for i, w1 in enumerate(whistles):
        for w2 in whistles[i + 1 :]:
            if (
                w1["start_time"] <= w2["end_time"]
                and w2["start_time"] <= w1["end_time"]
            ):
                overlaps += 1

    return {
        "whistle_count": len(whistles),
        "duration": round(duration, 2),
        "coverage": round(coverage, 1),
        "freq_min_khz": round(freq_min, 1),
        "freq_max_khz": round(freq_max, 1),
        "freq_mean_khz": round(freq_mean, 1),
        "freq_range_khz": round(freq_range, 1),
        "whistle_duration_mean_s": round(duration_mean, 3),
        "whistle_duration_std_s": round(duration_std, 3),
        "mean_gap_s": round(mean_gap, 3),
        "gap_variability": round(gap_std, 3),
        "overlaps": overlaps,
        "whistles_per_minute": round((len(whistles) / duration) * 60, 1),
    }


def process_file(file_path, rank, output_dir):
    """Process a single file and generate all assets."""
    print(f"📊 Processing rank {rank}: {Path(file_path).name}")

    # Read and process audio
    print(f"   Reading file...")
    ears_data = read_ears_file(file_path)
    audio_data = ears_data["data"]
    sample_rate = ears_data["fs"]
    metadata = {
        "time_start": str(ears_data["time_start"]),
        "duration": ears_data["duration"],
    }

    # Denoise
    print(f"   Denoising...")
    denoised = wavelet_denoise(audio_data, wavelet="db20")

    # Detect whistles
    print(f"   Detecting whistles...")
    whistles = detect_whistles(denoised, sample_rate)
    print(f"   Found {len(whistles)} whistles")

    # Calculate stats
    print(f"   Calculating statistics...")
    stats = calculate_statistics(whistles, audio_data, sample_rate)

    # Create output filenames
    base_name = f"rank_{rank:02d}_{Path(file_path).stem}"

    # Save audio files (raw and denoised)
    print(f"   Saving audio files...")
    audio_dir = output_dir / "audio"
    audio_dir.mkdir(exist_ok=True, parents=True)

    raw_wav = audio_dir / f"{base_name}_raw.wav"
    denoised_wav = audio_dir / f"{base_name}_denoised.wav"

    wavfile.write(raw_wav, sample_rate, audio_data.astype(np.float32))
    wavfile.write(denoised_wav, sample_rate, denoised.astype(np.float32))

    # Create visualizations
    print(f"   Creating spectrogram...")
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True, parents=True)

    spec_path = images_dir / f"{base_name}_spectrogram.png"
    wave_path = images_dir / f"{base_name}_waveform.png"

    create_spectrogram_image(
        denoised, sample_rate, spec_path, f"Rank {rank} - {len(whistles)} whistles"
    )

    print(f"   Creating waveform...")
    create_waveform_with_whistles(denoised, sample_rate, whistles, wave_path)

    print(f"   ✅ Rank {rank} complete!")

    return {
        "rank": rank,
        "filename": Path(file_path).name,
        "original_path": str(file_path),
        "audio_raw": f"audio/{raw_wav.name}",
        "audio_denoised": f"audio/{denoised_wav.name}",
        "spectrogram": f"images/{spec_path.name}",
        "waveform": f"images/{wave_path.name}",
        "stats": stats,
        "metadata": metadata,
    }


def create_summary_stats(all_files_data):
    """Create overall summary statistics."""
    total_whistles = sum(f["stats"]["whistle_count"] for f in all_files_data)
    total_duration = sum(f["stats"]["duration"] for f in all_files_data)

    all_freq_ranges = [f["stats"]["freq_range_khz"] for f in all_files_data]
    all_coverages = [f["stats"]["coverage"] for f in all_files_data]
    all_overlaps = sum(f["stats"]["overlaps"] for f in all_files_data)

    return {
        "total_files": len(all_files_data),
        "total_whistles": total_whistles,
        "total_duration_s": round(total_duration, 1),
        "avg_whistles_per_file": round(total_whistles / len(all_files_data), 1),
        "avg_coverage": round(np.mean(all_coverages), 1),
        "avg_freq_range_khz": round(np.mean(all_freq_ranges), 1),
        "total_overlaps": all_overlaps,
        "files_with_overlaps": sum(
            1 for f in all_files_data if f["stats"]["overlaps"] > 0
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate showcase from top results")
    parser.add_argument(
        "--checkpoint", required=True, help="Path to checkpoint/results JSON"
    )
    parser.add_argument(
        "--top", type=int, default=15, help="Number of top files to showcase"
    )
    parser.add_argument(
        "--output-dir", default="site/showcase", help="Output directory"
    )

    args = parser.parse_args()

    # Load results
    print(f"📂 Loading results from {args.checkpoint}")
    with open(args.checkpoint, "r") as f:
        results = json.load(f)

    # Get top files (handle both formats)
    if "top_files" in results:
        top_files = results["top_files"][: args.top]
    elif "results" in results:
        # Sort by interestingness_score and take top N
        sorted_results = sorted(
            results["results"],
            key=lambda x: x.get("interestingness_score", 0),
            reverse=True,
        )
        top_files = [
            {"file": r["file"], "score": r["interestingness_score"]}
            for r in sorted_results[: args.top]
        ]
    else:
        raise ValueError("Unknown results format - need 'top_files' or 'results' key")

    print(f"🎯 Processing top {len(top_files)} files...")

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)

    # Process each file
    showcase_data = []
    for i, file_info in enumerate(top_files, 1):
        try:
            file_data = process_file(file_info["file"], i, output_dir)
            file_data["score"] = file_info["score"]
            showcase_data.append(file_data)
        except Exception as e:
            print(f"❌ Error processing {file_info['file']}: {e}")
            continue

    # Create summary statistics
    summary = create_summary_stats(showcase_data)

    # Save showcase data
    showcase_json = {
        "generated": results.get("timestamp", "unknown"),
        "summary": summary,
        "files": showcase_data,
    }

    output_json = output_dir / "showcase_data.json"
    with open(output_json, "w") as f:
        json.dump(showcase_json, f, indent=2)

    print(f"\n✅ Showcase generated!")
    print(f"   📁 Output: {output_dir}")
    print(f"   🎵 Files: {len(showcase_data)}")
    print(f"   🎺 Total whistles: {summary['total_whistles']}")
    print(f"   📊 Data: {output_json}")


if __name__ == "__main__":
    main()
