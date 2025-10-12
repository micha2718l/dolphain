#!/usr/bin/env python3
"""
Quick-start script for finding interesting files in a hurry.

This is a simplified wrapper that runs the most common workflow:
1. Sample files from your drive
2. Find the most interesting ones
3. Generate a quick report

Usage:
    python quick_find.py /Volumes/ladcuno8tb0/

    # Custom sample size (default 1000 files)
    python quick_find.py /Volumes/ladcuno8tb0/ --n-files 500
"""

import sys
import argparse
from pathlib import Path
import time
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


def quick_find(
    data_dir: Path = None,
    file_list_path: Path = None,
    n_files: int = 1000,
    output_dir: Path = None,
    resume: bool = False,
):
    """
    Quick analysis to find top interesting files.

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
    print("🐬 QUICK FIND - INTERESTING EARS FILES")
    print("=" * 80)
    print(f"Sample size: {n_files} files")
    print(f"Output: {output_dir}")
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

    # Step 2: Quick analysis with enhanced scoring
    print("🔍 Step 2: Running enhanced analysis...")
    print(f"  🎯 Features: activity, diversity, SNR, complexity, patterns, overlaps")
    print(f"  Will save checkpoint every 10 files (safe to interrupt!)")
    start_time = time.time()

    files_to_process = [f for f in file_list if str(f) not in processed_files]
    total_files = len(file_list)
    already_done = len(processed_files)

    print(f"  📊 Status: {already_done}/{total_files} files already processed")
    print(f"  🚀 Processing {len(files_to_process)} remaining files...\n")

    def calculate_enhanced_interestingness(result, whistles, signal_clean, fs):
        """Calculate enhanced interestingness with multiple features."""
        score = 0.0
        n_whistles = result.get("n_whistles", 0)
        coverage = result.get("whistle_coverage_percent", 0)

        # Feature 1: Whistle activity (30 pts)
        score += min(15, (n_whistles / 30) * 15)  # Diminishing returns
        score += min(15, coverage * 0.15)

        # Feature 2: Whistle diversity (20 pts)
        if whistles and len(whistles) >= 2:
            freqs = [w.get("mean_freq", 0) for w in whistles]
            durations = [w.get("duration", 0) for w in whistles]
            freq_range = (max(freqs) - min(freqs)) if freqs else 0
            dur_std = np.std(durations) if durations else 0
            score += min(10, (freq_range / 10000) * 10)
            score += min(10, dur_std * 20)

        # Feature 3: Signal quality - SNR (15 pts)
        try:
            whistle_band = signal_clean[::10]
            fft = np.fft.rfft(whistle_band)
            power_spectrum = np.abs(fft) ** 2
            freq_bins = np.fft.rfftfreq(len(whistle_band), 1 / fs)

            whistle_mask = (freq_bins >= 5000) & (freq_bins <= 25000)
            noise_mask = (freq_bins >= 1000) & (freq_bins <= 5000)

            if np.any(whistle_mask) and np.any(noise_mask):
                signal_power = np.mean(power_spectrum[whistle_mask])
                noise_power = np.mean(power_spectrum[noise_mask])
                snr = 10 * np.log10(signal_power / (noise_power + 1e-10))
                score += min(15, max(0, (snr / 30) * 15))
        except:
            pass

        # Feature 4: Whistle complexity - FM rate (15 pts)
        if whistles:
            fm_scores = []
            for w in whistles[:10]:
                if "frequency" in w and len(w["frequency"]) > 3:
                    freq_diff = np.abs(np.diff(w["frequency"]))
                    if len(freq_diff) > 0:
                        fm_scores.append(np.mean(freq_diff))
            if fm_scores:
                mean_fm = np.mean(fm_scores)
                score += min(15, (mean_fm / 500) * 15)

        # Feature 5: Activity patterns (20 pts)
        if whistles and len(whistles) >= 3:
            start_times = np.array([w["start_time"] for w in whistles])
            gaps = np.diff(sorted(start_times))
            if len(gaps) > 0:
                gap_std = np.std(gaps)
                mean_gap = np.mean(gaps)
                score += min(10, (1.0 / (gap_std + 0.01)) * 2)  # Bursting
                score += min(10, max(0, (1.0 - mean_gap) * 10))  # Sustained

        # Bonus: Overlapping whistles (10 pts)
        if whistles and len(whistles) >= 2:
            overlaps = 0
            for i, w1 in enumerate(whistles[:-1]):
                for w2 in whistles[i + 1 :]:
                    if (
                        w1["start_time"] <= w2["end_time"]
                        and w2["start_time"] <= w1["end_time"]
                    ):
                        overlaps += 1
            score += min(10, overlaps * 2)

        return score

    for i, file_path in enumerate(files_to_process):
        overall_index = already_done + i
        try:
            # Read and process file
            data_dict = dolphain.read_ears_file(file_path)
            signal_clean = dolphain.wavelet_denoise(data_dict["data"], wavelet="db8")
            whistles = dolphain.detect_whistles(
                signal_clean,
                data_dict["fs"],
                power_threshold_percentile=85.0,
                min_duration=0.1,
            )

            # Calculate basic stats
            n_whistles = len(whistles)
            if n_whistles > 0:
                durations = [w["duration"] for w in whistles]
                mean_duration = float(np.mean(durations))
                total_duration = float(np.sum(durations))
                coverage = total_duration / data_dict["duration"] * 100
            else:
                mean_duration = 0.0
                total_duration = 0.0
                coverage = 0.0

            result = {
                "file": str(file_path),
                "filename": file_path.name,
                "n_whistles": n_whistles,
                "mean_whistle_duration": mean_duration,
                "total_whistle_duration": total_duration,
                "whistle_coverage_percent": coverage,
                "recording_duration": data_dict["duration"],
            }

            # Calculate enhanced interestingness score
            score = calculate_enhanced_interestingness(
                result, whistles, signal_clean, data_dict["fs"]
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

        # Progress updates every 10 files (more frequent than before!)
        if (overall_index + 1) % 10 == 0 or (overall_index + 1) == total_files:
            elapsed = time.time() - start_time
            files_done = overall_index + 1 - already_done
            if files_done > 0:
                rate = files_done / elapsed
                remaining_files = total_files - overall_index - 1
                remaining_time = remaining_files / rate if rate > 0 else 0

                # Calculate stats so far
                n_with_whistles = sum(1 for r in results if r.get("n_whistles", 0) > 0)
                hit_rate = (n_with_whistles / len(results) * 100) if results else 0

                print(
                    f"  ⏳ Progress: {overall_index + 1}/{total_files} ({(overall_index + 1)/total_files*100:.1f}%) "
                    f"| {rate:.1f} files/s | ETA: {remaining_time/60:.1f}m | "
                    f"Hit rate: {hit_rate:.0f}% | Checkpoint saved ✓"
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
                "results": results,
                "errors": errors,
            },
            f,
            indent=2,
        )

    # Save top files list
    top_20 = results[:20]
    with open(output_dir / "top_20_files.txt", "w") as f:
        f.write("TOP 20 MOST INTERESTING FILES\n")
        f.write("=" * 80 + "\n\n")
        f.write(
            f"{'Rank':<6} {'Score':<8} {'Whistles':<10} {'Coverage':<10} {'File'}\n"
        )
        f.write("-" * 80 + "\n")

        for i, result in enumerate(top_20, 1):
            score = result["interestingness_score"]
            whistles = result.get("n_whistles", 0)
            coverage = result.get("whistle_coverage_percent", 0)
            filename = result["filename"]

            f.write(
                f"{i:<6} {score:<8.1f} {whistles:<10} {coverage:<9.1f}% {filename}\n"
            )

        f.write("\n\nFull file paths:\n")
        f.write("-" * 80 + "\n")
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
    print(
        f"Files with whistles: {sum(1 for r in results if r.get('n_whistles', 0) > 0)}"
    )
    print(
        f"Mean whistles per file: {sum(r.get('n_whistles', 0) for r in results) / len(results):.2f}"
    )
    print()

    print("TOP 5 FILES:")
    for i, result in enumerate(results[:5], 1):
        score = result["interestingness_score"]
        whistles = result.get("n_whistles", 0)
        coverage = result.get("whistle_coverage_percent", 0)
        print(
            f"  {i}. Score: {score:.1f} | Whistles: {whistles} | Coverage: {coverage:.1f}%"
        )
        print(f"     {result['filename']}")

    print("\n" + "=" * 80)
    print("✅ QUICK FIND COMPLETE!")
    print("=" * 80)
    print(f"\nResults saved to: {output_dir}/")
    print(f"\nNext steps:")
    print(f"  1. Review top_20_files.txt")
    print(f"  2. Copy interesting files to working directory")
    print(
        f"  3. Run full analysis: python explore_interesting.py --results {output_dir}/results.json"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Quick find interesting EARS files",
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
        print(f"   Run: python parse_drive_listing.py")
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
