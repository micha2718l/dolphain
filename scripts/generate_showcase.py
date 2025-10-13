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
    """Create a clean spectrogram image without labels for easy scrubbing."""
    fig, ax = plt.subplots(figsize=(12, 3), facecolor="#0a0e27")
    ax.set_facecolor("#0a0e27")

    # Compute spectrogram
    f, t, Sxx = scipy_signal.spectrogram(
        audio_data, fs=sample_rate, nperseg=512, noverlap=480, window="hann"
    )

    # Convert to dB
    Sxx_dB = 10 * np.log10(Sxx + 1e-10)
    
    # Use imshow for MUCH faster rendering than pcolormesh
    im = ax.imshow(
        Sxx_dB,
        aspect='auto',
        origin='lower',
        cmap="viridis",
        vmin=-80,
        vmax=-20,
        extent=[t[0], t[-1], f[0] / 1000, f[-1] / 1000],
        interpolation='bilinear'
    )

    # Minimal labels - no ticks, just title
    ax.set_ylim([0, 50])
    ax.axis('off')  # Remove all axes

    if title:
        ax.text(0.5, 0.98, title, transform=ax.transAxes, 
                color='white', fontsize=11, ha='center', va='top')

    plt.tight_layout(pad=0)
    plt.subplots_adjust(left=0, right=1, top=0.95, bottom=0)
    plt.savefig(output_path, dpi=80, facecolor="#0a0e27", edgecolor="none", bbox_inches='tight', pad_inches=0.05)
    plt.close()


def create_waveform_image(audio_data, sample_rate, output_path):
    """Create a clean waveform image for scrubbing."""
    fig, ax = plt.subplots(figsize=(12, 1.5), facecolor="#0a0e27")
    ax.set_facecolor("#0a0e27")

    time = np.arange(len(audio_data)) / sample_rate
    
    # Plot waveform
    ax.plot(time, audio_data, color="#00d4ff", linewidth=0.5, alpha=0.8)
    ax.set_xlim([0, time[-1]])
    ax.set_ylim([audio_data.min() * 1.1, audio_data.max() * 1.1])
    
    # Remove axes for clean look
    ax.axis('off')

    plt.tight_layout(pad=0)
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(output_path, dpi=80, facecolor="#0a0e27", edgecolor="none", bbox_inches='tight', pad_inches=0.05)
    plt.close()


def create_waveform_with_whistles(audio_data, sample_rate, whistles, output_path):
    """Create waveform visualization with whistle overlays (legacy)."""
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


def process_file(file_path, rank, output_dir, result_data=None):
    """Process a single file and generate all assets."""
    print(f"📊 Processing rank {rank}: {Path(file_path).name}")

    # Read audio (skip if file doesn't exist)
    print(f"   Reading file...")
    try:
        ears_data = read_ears_file(file_path)
    except FileNotFoundError:
        print(f"   ⚠️  File not found, skipping...")
        return None
    
    audio_data = ears_data["data"]
    sample_rate = ears_data["fs"]
    metadata = {
        "time_start": str(ears_data["time_start"]),
        "duration": ears_data["duration"],
    }

    # Denoise quickly
    print(f"   Denoising...")
    denoised = wavelet_denoise(audio_data, wavelet="db8")  # Faster wavelet

    # Use pre-computed statistics from result_data if available
    if result_data:
        print(f"   Using pre-computed statistics...")
        stats = {
            "chirp_count": result_data.get("n_chirps", 0),
            "click_train_count": result_data.get("n_click_trains", 0),
            "total_clicks": result_data.get("total_clicks", 0),
            "duration": result_data.get("recording_duration", ears_data["duration"]),
            "chirp_coverage": result_data.get("chirp_coverage_percent", 0),
            "click_coverage": result_data.get("click_train_coverage_percent", 0),
            "mean_click_rate": result_data.get("mean_click_rate", 0),
        }
    else:
        # Fallback: detect features (slower path)
        print(f"   Detecting features...")
        whistles = detect_whistles(denoised, sample_rate)
        print(f"   Found {len(whistles)} whistles")
        stats = calculate_statistics(whistles, audio_data, sample_rate)

    # Create output filenames
    base_name = f"rank_{rank:02d}_{Path(file_path).stem}"

    # Save audio files (both raw and denoised)
    print(f"   Saving audio...")
    audio_dir = output_dir / "audio"
    audio_dir.mkdir(exist_ok=True, parents=True)

    # Save raw audio
    raw_wav = audio_dir / f"{base_name}_raw.wav"
    wavfile.write(raw_wav, sample_rate, audio_data.astype(np.float32))
    
    # Save denoised audio
    denoised_wav = audio_dir / f"{base_name}.wav"
    wavfile.write(denoised_wav, sample_rate, denoised.astype(np.float32))

    # Create visualizations - spectrogram and waveform for BOTH raw and denoised
    print(f"   Creating visualizations...")
    images_dir = output_dir / "images"
    images_dir.mkdir(exist_ok=True, parents=True)

    # Determine title based on stats
    if result_data:
        n_chirps = result_data.get("n_chirps", 0)
        n_clicks = result_data.get("total_clicks", 0)
        title_base = f"Rank {rank} - {n_chirps} chirps, {n_clicks} clicks"
    else:
        title_base = f"Rank {rank}"
    
    # Create DENOISED visualizations
    spec_denoised_path = images_dir / f"{base_name}_spectrogram_denoised.png"
    create_spectrogram_image(denoised, sample_rate, spec_denoised_path, f"{title_base} (Denoised)")
    
    waveform_denoised_path = images_dir / f"{base_name}_waveform_denoised.png"
    create_waveform_image(denoised, sample_rate, waveform_denoised_path)
    
    # Create RAW visualizations
    spec_raw_path = images_dir / f"{base_name}_spectrogram_raw.png"
    create_spectrogram_image(audio_data, sample_rate, spec_raw_path, f"{title_base} (Raw)")
    
    waveform_raw_path = images_dir / f"{base_name}_waveform_raw.png"
    create_waveform_image(audio_data, sample_rate, waveform_raw_path)

    print(f"   ✅ Rank {rank} complete!")

    return {
        "rank": rank,
        "filename": Path(file_path).name,
        "original_path": str(file_path),
        "audio_raw": f"audio/{raw_wav.name}",
        "audio_denoised": f"audio/{denoised_wav.name}",
        "spectrogram_denoised": f"images/{spec_denoised_path.name}",
        "waveform_denoised": f"images/{waveform_denoised_path.name}",
        "spectrogram_raw": f"images/{spec_raw_path.name}",
        "waveform_raw": f"images/{waveform_raw_path.name}",
        "stats": stats,
        "metadata": metadata,
    }


def create_summary_stats(all_files_data):
    """Create overall summary statistics."""
    # Handle both old whistle format and new chirp/click format
    if all_files_data and "chirp_count" in all_files_data[0]["stats"]:
        # New format: chirps and clicks
        total_chirps = sum(f["stats"]["chirp_count"] for f in all_files_data)
        total_clicks = sum(f["stats"]["total_clicks"] for f in all_files_data)
        total_duration = sum(f["stats"]["duration"] for f in all_files_data)
        
        return {
            "total_files": len(all_files_data),
            "total_chirps": total_chirps,
            "total_clicks": total_clicks,
            "total_duration_s": round(total_duration, 1),
            "avg_chirps_per_file": round(total_chirps / len(all_files_data), 1),
            "avg_clicks_per_file": round(total_clicks / len(all_files_data), 1),
        }
    else:
        # Old format: whistles
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
    results_list = None
    if "top_files" in results:
        top_files = results["top_files"][: args.top]
    elif "results" in results:
        # Sort by interestingness_score and take top N
        results_list = results["results"]
        sorted_results = sorted(
            results_list,
            key=lambda x: x.get("interestingness_score", 0),
            reverse=True,
        )
        top_files = [
            {"file": r["file"], "score": r["interestingness_score"], "data": r}
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
            # Pass the result data if available for faster processing
            result_data = file_info.get("data", None)
            file_data = process_file(file_info["file"], i, output_dir, result_data)
            if file_data:  # Skip if file not found
                file_data["score"] = file_info["score"]
                showcase_data.append(file_data)
        except Exception as e:
            print(f"❌ Error processing {file_info['file']}: {e}")
            import traceback
            traceback.print_exc()
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
    if "total_chirps" in summary:
        print(f"   🎺 Total chirps: {summary['total_chirps']}")
        print(f"   🔊 Total clicks: {summary['total_clicks']}")
    else:
        print(f"   🎺 Total whistles: {summary['total_whistles']}")
    print(f"   📊 Data: {output_json}")


if __name__ == "__main__":
    main()
