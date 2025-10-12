#!/usr/bin/env python3
"""
Monitor quick_find.py progress and show live top 5 results.

Usage:
    python monitor_quick_find.py
    python monitor_quick_find.py --output-dir outputs/results/large_run
    python monitor_quick_find.py --output-dir outputs/results/large_run --refresh 10
"""

import sys
import argparse
import json
import time
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np


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


def plot_top_5(checkpoint_file, ax1, ax2, ax3):
    """Update plots with current top 5 files."""
    data = load_checkpoint(checkpoint_file)

    if data is None:
        ax1.clear()
        ax1.text(
            0.5,
            0.5,
            "Waiting for checkpoint file...\n\n" + f"Looking for: {checkpoint_file}",
            ha="center",
            va="center",
            fontsize=12,
        )
        ax1.axis("off")
        ax2.axis("off")
        ax3.axis("off")
        return

    results = data.get("results", [])

    if not results:
        ax1.clear()
        ax1.text(
            0.5,
            0.5,
            "No results yet...\nWaiting for first file to complete.",
            ha="center",
            va="center",
            fontsize=12,
        )
        ax1.axis("off")
        ax2.axis("off")
        ax3.axis("off")
        return

    # Sort by interestingness score
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

    # Plot 1: Top 5 scores (bar chart)
    ax1.clear()
    filenames = [
        r["filename"][:15] + "..." if len(r["filename"]) > 15 else r["filename"]
        for r in top_5
    ]
    scores = [r.get("interestingness_score", 0) for r in top_5]
    colors = plt.cm.viridis(np.linspace(0.8, 0.3, len(scores)))

    bars = ax1.barh(range(len(scores)), scores, color=colors)
    ax1.set_yticks(range(len(scores)))
    ax1.set_yticklabels([f"#{i+1} {name}" for i, name in enumerate(filenames)])
    ax1.set_xlabel("Interestingness Score", fontsize=10, fontweight="bold")
    ax1.set_title(
        f"🐬 Top 5 Files (Live) - {n_files} files analyzed",
        fontsize=12,
        fontweight="bold",
        pad=10,
    )
    ax1.invert_yaxis()
    ax1.grid(axis="x", alpha=0.3)

    # Add score labels on bars
    for i, (bar, score) in enumerate(zip(bars, scores)):
        ax1.text(
            score + 1,
            bar.get_y() + bar.get_height() / 2,
            f"{score:.1f}",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    # Plot 2: Whistles vs Coverage scatter
    ax2.clear()
    for i, r in enumerate(top_5):
        whistles = r.get("n_whistles", 0)
        coverage = r.get("whistle_coverage_percent", 0)
        score = r.get("interestingness_score", 0)

        # Size based on score
        size = 100 + score * 10
        ax2.scatter(
            whistles,
            coverage,
            s=size,
            alpha=0.6,
            color=colors[i],
            edgecolors="black",
            linewidth=2,
            label=f"#{i+1}",
        )

    ax2.set_xlabel("Number of Whistles", fontsize=10, fontweight="bold")
    ax2.set_ylabel("Coverage (%)", fontsize=10, fontweight="bold")
    ax2.set_title("Whistles vs Coverage", fontsize=11, fontweight="bold")
    ax2.grid(alpha=0.3)
    ax2.legend(loc="lower right", fontsize=8)

    # Plot 3: Stats summary (text)
    ax3.clear()
    ax3.axis("off")

    stats_text = f"""
    📊 ANALYSIS STATISTICS
    {'='*35}
    
    Files Processed:     {n_files:,}
    Files with Whistles: {n_with_whistles:,} ({hit_rate:.1f}%)
    Mean Whistles/File:  {mean_whistles:.1f}
    
    🏆 TOP FILE DETAILS
    {'='*35}
    """

    # Add top 5 details
    for i, r in enumerate(top_5, 1):
        score = r.get("interestingness_score", 0)
        whistles = r.get("n_whistles", 0)
        coverage = r.get("whistle_coverage_percent", 0)
        filename = r["filename"]

        stats_text += f"""
    #{i}. {filename}
       Score: {score:.1f} | Whistles: {whistles} | Coverage: {coverage:.1f}%
    """

    # Add timestamp
    last_updated = data.get("last_updated", time.time())
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_updated))
    stats_text += f"\n\n    Last Updated: {time_str}"

    ax3.text(
        0.05,
        0.95,
        stats_text,
        transform=ax3.transAxes,
        fontsize=9,
        verticalalignment="top",
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.3),
    )


def monitor_live(output_dir, refresh_interval=5):
    """Monitor with live updating plot."""
    checkpoint_file = output_dir / "checkpoint.json"

    print("=" * 80)
    print("🐬 QUICK FIND LIVE MONITOR")
    print("=" * 80)
    print(f"Watching: {checkpoint_file}")
    print(f"Refresh: Every {refresh_interval} seconds")
    print(f"Press Ctrl+C to stop")
    print("=" * 80)
    print()

    # Create figure with 3 subplots
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, :])  # Top 5 bar chart (full width)
    ax2 = fig.add_subplot(gs[1, 0])  # Scatter plot
    ax3 = fig.add_subplot(gs[1, 1])  # Stats text

    fig.suptitle("Quick Find Live Monitor", fontsize=16, fontweight="bold")

    # Animation function
    def update(frame):
        try:
            plot_top_5(checkpoint_file, ax1, ax2, ax3)
        except Exception as e:
            print(f"Error updating plot: {e}")

    # Create animation
    ani = FuncAnimation(
        fig, update, interval=refresh_interval * 1000, cache_frame_data=False
    )

    plt.tight_layout()
    plt.show()


def monitor_once(output_dir):
    """Single snapshot of current status."""
    checkpoint_file = output_dir / "checkpoint.json"

    print("=" * 80)
    print("🐬 QUICK FIND SNAPSHOT")
    print("=" * 80)
    print(f"Reading: {checkpoint_file}")
    print()

    data = load_checkpoint(checkpoint_file)

    if data is None:
        print("❌ No checkpoint file found or invalid JSON")
        print(f"   Looking for: {checkpoint_file}")
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

    # Print summary
    print(f"Files Processed:     {n_files:,}")
    print(f"Files with Whistles: {n_with_whistles:,} ({hit_rate:.1f}%)")
    print(f"Mean Whistles/File:  {mean_whistles:.1f}")
    print(f"Errors:              {len(errors)}")
    print()

    print("🏆 TOP 5 FILES:")
    print("-" * 80)
    for i, r in enumerate(top_5, 1):
        score = r.get("interestingness_score", 0)
        whistles = r.get("n_whistles", 0)
        coverage = r.get("whistle_coverage_percent", 0)
        filename = r["filename"]

        print(
            f"{i}. Score: {score:5.1f} | Whistles: {whistles:3d} | "
            f"Coverage: {coverage:5.1f}% | {filename}"
        )

    print()
    print("=" * 80)

    # Create static plot
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])

    fig.suptitle("Quick Find Snapshot", fontsize=16, fontweight="bold")

    plot_top_5(checkpoint_file, ax1, ax2, ax3)

    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Monitor quick_find.py progress in real-time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Live monitor (auto-refreshing every 5 seconds)
  python monitor_quick_find.py
  
  # Custom output directory
  python monitor_quick_find.py --output-dir outputs/results/large_run
  
  # Faster refresh (every 2 seconds)
  python monitor_quick_find.py --refresh 2
  
  # Single snapshot (no auto-refresh)
  python monitor_quick_find.py --once
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
    parser.add_argument(
        "--once",
        action="store_true",
        help="Show snapshot once and exit (no live updates)",
    )

    args = parser.parse_args()

    # Check if output directory exists
    if not args.output_dir.exists():
        print(f"⚠️  Warning: Output directory not found: {args.output_dir}")
        print(f"   Creating directory...")
        args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.once:
        monitor_once(args.output_dir)
    else:
        monitor_live(args.output_dir, args.refresh)


if __name__ == "__main__":
    main()
