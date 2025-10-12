#!/usr/bin/env python3
"""
Simple text-based monitor for quick_find.py progress.
No matplotlib required - runs in terminal.

Usage:
    python monitor_text.py
    python monitor_text.py --output-dir outputs/results/large_run
"""

import sys
import argparse
import json
import time
from pathlib import Path
import os


def clear_screen():
    """Clear terminal screen."""
    os.system("clear" if os.name != "nt" else "cls")


def load_checkpoint(checkpoint_file):
    """Load current checkpoint data."""
    if not checkpoint_file.exists():
        return None

    try:
        with open(checkpoint_file, "r") as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def print_status(checkpoint_file):
    """Print current status."""
    clear_screen()

    print("=" * 80)
    print("🐬 QUICK FIND LIVE MONITOR (Text Mode)")
    print("=" * 80)
    print(f"Watching: {checkpoint_file}")
    print(f"Press Ctrl+C to stop")
    print(f"Last refresh: {time.strftime('%H:%M:%S')}")
    print("=" * 80)
    print()

    data = load_checkpoint(checkpoint_file)

    if data is None:
        print("⏳ Waiting for checkpoint file...")
        print(f"   Looking for: {checkpoint_file}")
        print()
        print("   Make sure quick_find.py is running!")
        return

    results = data.get("results", [])
    errors = data.get("errors", [])

    if not results:
        print("⏳ No results yet - waiting for first file to complete")
        return

    # Sort and get top 5
    results_sorted = sorted(
        results, key=lambda x: x.get("interestingness_score", 0), reverse=True
    )
    top_5 = results_sorted[:5]

    # Calculate stats
    n_files = len(results)
    n_with_whistles = sum(1 for r in results if r.get("n_whistles", 0) > 0)
    hit_rate = (n_with_whistles / n_files * 100) if n_files > 0 else 0
    mean_whistles = (
        sum(r.get("n_whistles", 0) for r in results) / n_files if n_files > 0 else 0
    )

    # Print stats
    print("📊 PROGRESS STATISTICS")
    print("-" * 80)
    print(f"  Files Processed:       {n_files:,}")
    print(f"  Files with Whistles:   {n_with_whistles:,} ({hit_rate:.1f}%)")
    print(f"  Mean Whistles/File:    {mean_whistles:.1f}")
    print(f"  Errors:                {len(errors)}")
    print()

    # Print top 5 with fancy bars
    print("🏆 TOP 5 FILES (LIVE)")
    print("-" * 80)

    max_score = max(r.get("interestingness_score", 0) for r in top_5) if top_5 else 100

    for i, r in enumerate(top_5, 1):
        score = r.get("interestingness_score", 0)
        whistles = r.get("n_whistles", 0)
        coverage = r.get("whistle_coverage_percent", 0)
        filename = r["filename"]

        # Create bar graph
        bar_length = int((score / max_score) * 40) if max_score > 0 else 0
        bar = "█" * bar_length + "░" * (40 - bar_length)

        print(f"#{i}. {filename}")
        print(f"    Score: {score:5.1f} {bar}")
        print(f"    Whistles: {whistles:3d} | Coverage: {coverage:5.1f}%")
        print()

    # Progress bar for overall completion (if we know total)
    print("=" * 80)
    print()

    # Add timestamp
    last_updated = data.get("last_updated", time.time())
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_updated))
    print(f"Last checkpoint update: {time_str}")


def monitor_live(output_dir, refresh_interval=5):
    """Monitor with live updating in terminal."""
    checkpoint_file = output_dir / "checkpoint.json"

    try:
        while True:
            print_status(checkpoint_file)
            time.sleep(refresh_interval)
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped")
        print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Monitor quick_find.py progress in terminal (text-only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor default output directory
  python monitor_text.py
  
  # Monitor custom directory
  python monitor_text.py --output-dir outputs/results/large_run
  
  # Faster refresh (every 2 seconds)
  python monitor_text.py --refresh 2
        """,
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("quick_find_results"),
        help="Output directory where checkpoint is saved (default: quick_find_results)",
    )
    parser.add_argument(
        "--refresh",
        type=int,
        default=5,
        help="Refresh interval in seconds (default: 5)",
    )

    args = parser.parse_args()

    monitor_live(args.output_dir, args.refresh)


if __name__ == "__main__":
    main()
