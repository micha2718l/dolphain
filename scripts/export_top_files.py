#!/usr/bin/env python3
"""
Export top N files from quick_find checkpoint to WAV + plots.

This script:
1. Reads the current top files from checkpoint
2. Converts each to WAV (raw + denoised)
3. Creates detailed visualization plots
4. Saves everything to an organized output directory

Usage:
    python export_top_files.py
    python export_top_files.py --checkpoint outputs/results/large_run/checkpoint.json --top 5
    python export_top_files.py --checkpoint outputs/results/large_run/results.json --top 10
"""

import sys
import argparse
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

sys.path.insert(0, str(Path(__file__).parent.parent))
import dolphain


def load_results(checkpoint_path):
    """Load results from checkpoint or final results file."""
    if not checkpoint_path.exists():
        print(f"❌ File not found: {checkpoint_path}")
        return None

    try:
        with open(checkpoint_path, "r") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in: {checkpoint_path}")
        return None


def create_detailed_plot(file_path, output_path, file_info):
    """Create detailed visualization with raw, denoised, and whistle overlay."""
    print(f"  📊 Creating plot for {file_path.name}...")

    try:
        # Read file
        data_dict = dolphain.read_ears_file(file_path)
        data = data_dict["data"]
        fs = data_dict["fs"]

        # Denoise
        denoised = dolphain.wavelet_denoise(data, wavelet="db20")

        # Detect whistles
        whistles = dolphain.detect_whistles(denoised, fs)

        # Create figure
        fig, axes = plt.subplots(3, 2, figsize=(16, 12))
        fig.suptitle(
            f"Top File: {file_path.name}\n"
            f'Score: {file_info.get("interestingness_score", 0):.1f} | '
            f'Whistles: {file_info.get("n_whistles", 0)} | '
            f'Coverage: {file_info.get("whistle_coverage_percent", 0):.1f}%',
            fontsize=14,
            fontweight="bold",
        )

        # Calculate time array
        duration = len(data) / fs
        time = np.linspace(0, duration, len(data))

        # Plot 1: Raw waveform
        axes[0, 0].plot(time, data, linewidth=0.5, alpha=0.7)
        axes[0, 0].set_title("Raw Waveform", fontweight="bold")
        axes[0, 0].set_xlabel("Time (s)")
        axes[0, 0].set_ylabel("Amplitude")
        axes[0, 0].grid(alpha=0.3)

        # Plot 2: Denoised waveform
        axes[0, 1].plot(time, denoised, linewidth=0.5, alpha=0.7, color="green")
        axes[0, 1].set_title("Denoised Waveform", fontweight="bold")
        axes[0, 1].set_xlabel("Time (s)")
        axes[0, 1].set_ylabel("Amplitude")
        axes[0, 1].grid(alpha=0.3)

        # Plot 3: Raw spectrogram
        spec_data = axes[1, 0].specgram(
            data, Fs=fs, NFFT=512, noverlap=256, cmap="viridis"
        )
        axes[1, 0].set_title("Raw Spectrogram", fontweight="bold")
        axes[1, 0].set_xlabel("Time (s)")
        axes[1, 0].set_ylabel("Frequency (Hz)")
        axes[1, 0].set_ylim(0, 50000)

        # Plot 4: Denoised spectrogram
        axes[1, 1].specgram(denoised, Fs=fs, NFFT=512, noverlap=256, cmap="viridis")
        axes[1, 1].set_title("Denoised Spectrogram", fontweight="bold")
        axes[1, 1].set_xlabel("Time (s)")
        axes[1, 1].set_ylabel("Frequency (Hz)")
        axes[1, 1].set_ylim(0, 50000)

        # Plot 5: Denoised spectrogram with whistle overlay (zoomed to whistle band)
        axes[2, 0].specgram(denoised, Fs=fs, NFFT=512, noverlap=256, cmap="viridis")

        # Overlay whistles
        if whistles:
            for whistle in whistles:
                start = whistle["start_time"]
                end = whistle["end_time"]
                f_min = whistle["min_freq"]
                f_max = whistle["max_freq"]

                # Draw rectangle around whistle
                rect_time = [start, end, end, start, start]
                rect_freq = [f_min, f_min, f_max, f_max, f_min]
                axes[2, 0].plot(rect_time, rect_freq, "r-", linewidth=2, alpha=0.8)

        axes[2, 0].set_title(
            f"Whistle Detection ({len(whistles)} whistles)", fontweight="bold"
        )
        axes[2, 0].set_xlabel("Time (s)")
        axes[2, 0].set_ylabel("Frequency (Hz)")
        axes[2, 0].set_ylim(5000, 25000)  # Zoom to whistle band

        # Plot 6: Statistics and info
        axes[2, 1].axis("off")

        stats_text = f"""
FILE INFORMATION
{'='*50}

Filename:        {file_path.name}
Duration:        {duration:.2f} seconds
Sample Rate:     {fs:,} Hz
Samples:         {len(data):,}

ANALYSIS RESULTS
{'='*50}

Interestingness: {file_info.get('interestingness_score', 0):.1f} / 100
Whistles:        {file_info.get('n_whistles', 0)}
Coverage:        {file_info.get('whistle_coverage_percent', 0):.1f}%
Mean Duration:   {file_info.get('whistle_mean_duration', 0):.2f} s

WHISTLE DETAILS
{'='*50}
"""

        if whistles:
            # Get some whistle stats
            durations = [w["end_time"] - w["start_time"] for w in whistles[:5]]
            freqs = [(w["min_freq"] + w["max_freq"]) / 2 for w in whistles[:5]]

            stats_text += f"\nFirst 5 whistles:\n"
            for i, (dur, freq) in enumerate(zip(durations, freqs), 1):
                stats_text += f"  {i}. Duration: {dur:.2f}s, Freq: {freq:.0f} Hz\n"
        else:
            stats_text += "\nNo whistles detected\n"

        axes[2, 1].text(
            0.05,
            0.95,
            stats_text,
            transform=axes[2, 1].transAxes,
            fontsize=9,
            verticalalignment="top",
            family="monospace",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.3),
        )

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        print(f"     ✓ Saved plot: {output_path}")
        return True

    except Exception as e:
        import traceback

        print(f"     ❌ Error creating plot: {e}")
        print(f"     Full traceback:")
        traceback.print_exc()
        return False


def convert_to_wav(file_path, output_dir, file_info):
    """Convert EARS file to WAV (both raw and denoised)."""
    print(f"  🔊 Converting to WAV: {file_path.name}...")

    try:
        # Read file
        data_dict = dolphain.read_ears_file(file_path)
        data = data_dict["data"]
        fs = data_dict["fs"]

        # Normalize raw data to int16 range
        raw_normalized = np.int16(data / np.max(np.abs(data)) * 32767 * 0.9)

        # Denoise
        denoised = dolphain.wavelet_denoise(data, wavelet="db20")
        denoised_normalized = np.int16(
            denoised / np.max(np.abs(denoised)) * 32767 * 0.9
        )

        # Save WAV files
        raw_path = output_dir / f"{file_path.stem}_raw.wav"
        denoised_path = output_dir / f"{file_path.stem}_denoised.wav"

        wavfile.write(raw_path, fs, raw_normalized)
        wavfile.write(denoised_path, fs, denoised_normalized)

        print(f"     ✓ Saved WAV: {raw_path.name}")
        print(f"     ✓ Saved WAV: {denoised_path.name}")
        return True

    except Exception as e:
        import traceback

        print(f"     ❌ Error converting to WAV: {e}")
        print(f"     Full traceback:")
        traceback.print_exc()
        return False


def export_top_files(checkpoint_path, top_n=5, output_base_dir=None):
    """Export top N files to WAV and plots."""

    print("=" * 80)
    print("🐬 EXPORT TOP FILES")
    print("=" * 80)
    print(f"Checkpoint: {checkpoint_path}")
    print(f"Top files:  {top_n}")
    print()

    # Load data
    data = load_results(checkpoint_path)
    if data is None:
        return

    results = data.get("results", [])

    if not results:
        print("❌ No results found in checkpoint")
        return

    # Sort by score and get top N
    results_sorted = sorted(
        results, key=lambda x: x.get("interestingness_score", 0), reverse=True
    )
    top_files = results_sorted[:top_n]

    print(f"Found {len(results)} total files")
    print(f"Exporting top {len(top_files)} files")
    print()

    # Create output directory
    if output_base_dir is None:
        timestamp = (
            checkpoint_path.parent.name
            if checkpoint_path.parent.name != "."
            else "export"
        )
        output_base_dir = Path("outputs") / "exports" / timestamp

    audio_dir = output_base_dir / "audio"
    plots_dir = output_base_dir / "plots"

    audio_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)

    print(f"Output directory: {output_base_dir}")
    print(f"  Audio: {audio_dir}")
    print(f"  Plots: {plots_dir}")
    print()

    # Process each file
    success_count = 0
    for i, file_info in enumerate(top_files, 1):
        file_path = Path(file_info["file"])
        score = file_info.get("interestingness_score", 0)
        whistles = file_info.get("n_whistles", 0)
        coverage = file_info.get("whistle_coverage_percent", 0)

        print(f"[{i}/{len(top_files)}] Processing: {file_path.name}")
        print(
            f"     Score: {score:.1f} | Whistles: {whistles} | Coverage: {coverage:.1f}%"
        )

        if not file_path.exists():
            print(f"     ⚠️  File not found: {file_path}")
            print(f"     Skipping...")
            continue

        # Create plot
        plot_path = plots_dir / f"rank{i:02d}_{file_path.stem}.png"
        plot_success = create_detailed_plot(file_path, plot_path, file_info)

        # Convert to WAV
        wav_success = convert_to_wav(file_path, audio_dir, file_info)

        if plot_success and wav_success:
            success_count += 1

        print()

    # Create summary file
    summary_path = output_base_dir / "README.txt"
    with open(summary_path, "w") as f:
        f.write("=" * 80 + "\n")
        f.write("TOP FILES EXPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Source: {checkpoint_path}\n")
        f.write(f"Exported: {len(top_files)} files\n")
        f.write(f"Date: {Path(__file__).stat().st_mtime}\n\n")
        f.write("FILES:\n")
        f.write("-" * 80 + "\n\n")

        for i, file_info in enumerate(top_files, 1):
            score = file_info.get("interestingness_score", 0)
            whistles = file_info.get("n_whistles", 0)
            coverage = file_info.get("whistle_coverage_percent", 0)
            filename = file_info["filename"]

            f.write(f"Rank {i}: {filename}\n")
            f.write(f"  Score: {score:.1f}\n")
            f.write(f"  Whistles: {whistles}\n")
            f.write(f"  Coverage: {coverage:.1f}%\n")
            f.write(f"  Audio: audio/{Path(filename).stem}_raw.wav\n")
            f.write(f"         audio/{Path(filename).stem}_denoised.wav\n")
            f.write(f"  Plot:  plots/rank{i:02d}_{Path(filename).stem}.png\n\n")

    print("=" * 80)
    print("✅ EXPORT COMPLETE!")
    print("=" * 80)
    print(f"Successfully exported: {success_count}/{len(top_files)} files")
    print()
    print(f"Output directory: {output_base_dir}")
    print(f"  Audio files:  {audio_dir}")
    print(f"  Plot files:   {plots_dir}")
    print(f"  Summary:      {summary_path}")
    print()
    print("Next steps:")
    print(f"  1. Open plots: open {plots_dir}")
    print(f"  2. Listen:     open {audio_dir}")
    print(f"  3. Review:     cat {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Export top files from quick_find to WAV + plots",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export top 5 from running checkpoint
  python export_top_files.py --checkpoint outputs/results/large_run/checkpoint.json
  
  # Export top 5 from completed results
  python export_top_files.py --checkpoint outputs/results/large_run/results.json
  
  # Export top 10 files
  python export_top_files.py --checkpoint quick_find_results/checkpoint.json --top 10
  
  # Custom output directory
  python export_top_files.py --checkpoint results.json --output-dir my_exports/
        """,
    )

    parser.add_argument(
        "--checkpoint", type=Path, help="Path to checkpoint.json or results.json file"
    )
    parser.add_argument(
        "--top", type=int, default=5, help="Number of top files to export (default: 5)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory (default: outputs/exports/<timestamp>)",
    )

    args = parser.parse_args()

    # If no checkpoint specified, look for common locations
    if not args.checkpoint:
        # Try common locations
        candidates = [
            Path("quick_find_results/checkpoint.json"),
            Path("quick_find_results/results.json"),
            Path("outputs/results/large_run/checkpoint.json"),
            Path("outputs/results/large_run/results.json"),
        ]

        for candidate in candidates:
            if candidate.exists():
                print(f"📂 Found checkpoint: {candidate}")
                args.checkpoint = candidate
                break

        if not args.checkpoint:
            print("❌ No checkpoint file specified and none found in common locations")
            print("\nTry:")
            print("  python export_top_files.py --checkpoint <path-to-checkpoint.json>")
            print("\nCommon locations:")
            for c in candidates:
                print(f"  - {c}")
            sys.exit(1)

    if not args.checkpoint.exists():
        print(f"❌ Checkpoint file not found: {args.checkpoint}")
        sys.exit(1)

    export_top_files(args.checkpoint, args.top, args.output_dir)


if __name__ == "__main__":
    main()
