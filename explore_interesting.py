#!/usr/bin/env python3
"""
Interactive explorer for interesting EARS files.

Creates detailed visualizations and reports for top-ranked files,
making it easy to review and select the best examples for publication,
presentations, or further analysis.

Usage:
    python explore_interesting.py --results interesting_files_analysis/interesting_files.json
    python explore_interesting.py --results interesting_files_analysis/interesting_files.json --top 10
"""

import sys
import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


def create_detailed_plot(file_path: Path, output_path: Path = None):
    """
    Create comprehensive visualization of a single file.
    
    Shows:
    - Waveform (raw and denoised)
    - Spectrogram
    - Whistle detections overlaid
    - Power spectral density
    - Temporal energy profile
    """
    # Read data
    data = dolphain.read_ears_file(file_path)
    signal = data['data']
    sample_rate = data['sample_rate']
    duration = data['duration']
    
    # Process
    signal_clean = dolphain.wavelet_denoise(signal, wavelet='db8')
    whistles = dolphain.detect_whistles(
        signal_clean,
        sample_rate=sample_rate,
        power_threshold_percentile=85.0,
        min_duration=0.1
    )
    
    # Create figure
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(4, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Title
    fig.suptitle(f"Detailed Analysis: {file_path.name}\n"
                f"Duration: {duration:.2f}s | Whistles: {len(whistles)} | "
                f"Coverage: {sum(w['duration'] for w in whistles)/duration*100:.1f}%",
                fontsize=14, fontweight='bold')
    
    # 1. Raw waveform
    ax1 = fig.add_subplot(gs[0, :])
    time_axis = np.arange(len(signal)) / sample_rate
    ax1.plot(time_axis, signal, 'b-', alpha=0.6, linewidth=0.5)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Raw Waveform')
    ax1.grid(True, alpha=0.3)
    
    # 2. Denoised waveform with whistle markers
    ax2 = fig.add_subplot(gs[1, :])
    ax2.plot(time_axis, signal_clean, 'g-', alpha=0.6, linewidth=0.5)
    
    # Mark whistles
    for whistle in whistles:
        start_time = whistle['start_idx'] / sample_rate
        end_time = start_time + whistle['duration']
        ax2.axvspan(start_time, end_time, alpha=0.3, color='red', label='Whistle' if whistles.index(whistle) == 0 else '')
    
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude')
    ax2.set_title(f'Denoised Waveform with Whistle Detections (n={len(whistles)})')
    ax2.grid(True, alpha=0.3)
    if whistles:
        ax2.legend()
    
    # 3. Spectrogram
    ax3 = fig.add_subplot(gs[2, :])
    dolphain.plot_spectrogram(
        signal_clean,
        sample_rate,
        title='Spectrogram (Denoised)',
        ax=ax3
    )
    
    # Overlay whistle detections on spectrogram
    for whistle in whistles:
        start_time = whistle['start_idx'] / sample_rate
        end_time = start_time + whistle['duration']
        ax3.axvline(start_time, color='red', linestyle='--', alpha=0.5, linewidth=1)
        ax3.axvline(end_time, color='red', linestyle='--', alpha=0.5, linewidth=1)
    
    # 4. Power Spectral Density
    ax4 = fig.add_subplot(gs[3, 0])
    from scipy import signal as scipy_signal
    freqs, psd = scipy_signal.welch(signal_clean, fs=sample_rate, nperseg=4096)
    ax4.semilogy(freqs / 1000, psd)
    ax4.set_xlabel('Frequency (kHz)')
    ax4.set_ylabel('Power Spectral Density')
    ax4.set_title('Power Spectral Density')
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim([0, 50])
    
    # Highlight whistle bands
    ax4.axvspan(5, 25, alpha=0.2, color='yellow', label='Whistle Band')
    ax4.legend()
    
    # 5. Temporal Energy Profile
    ax5 = fig.add_subplot(gs[3, 1])
    window_size = int(sample_rate * 0.1)  # 100ms windows
    n_windows = len(signal_clean) // window_size
    window_energies = []
    window_times = []
    
    for i in range(n_windows):
        start = i * window_size
        end = start + window_size
        window = signal_clean[start:end]
        energy = np.sum(window ** 2)
        window_energies.append(energy)
        window_times.append((start + end) / 2 / sample_rate)
    
    ax5.plot(window_times, window_energies, 'b-', linewidth=2)
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('Energy')
    ax5.set_title('Temporal Energy Profile (100ms windows)')
    ax5.grid(True, alpha=0.3)
    
    # Mark whistle regions
    for whistle in whistles:
        start_time = whistle['start_idx'] / sample_rate
        end_time = start_time + whistle['duration']
        ax5.axvspan(start_time, end_time, alpha=0.2, color='red')
    
    # Save or show
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def create_comparison_plot(results: list, output_path: Path):
    """
    Create comparison plot of top N files.
    """
    # Sort by score
    results = sorted(results, key=lambda x: x.get('interestingness_score', 0), reverse=True)
    top_n = min(20, len(results))
    top_results = results[:top_n]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Comparison of Top {top_n} Most Interesting Files', fontsize=14, fontweight='bold')
    
    # Extract data
    scores = [r['interestingness_score'] for r in top_results]
    whistles = [r.get('n_whistles', 0) for r in top_results]
    coverage = [r.get('whistle_coverage_percent', 0) for r in top_results]
    files = [Path(r['file']).name[:20] for r in top_results]  # Truncate names
    
    # 1. Interestingness scores
    axes[0, 0].barh(range(top_n), scores, color='steelblue')
    axes[0, 0].set_yticks(range(top_n))
    axes[0, 0].set_yticklabels([f"#{i+1}" for i in range(top_n)])
    axes[0, 0].set_xlabel('Interestingness Score')
    axes[0, 0].set_title('Overall Scores')
    axes[0, 0].invert_yaxis()
    axes[0, 0].grid(True, alpha=0.3, axis='x')
    
    # 2. Number of whistles
    axes[0, 1].barh(range(top_n), whistles, color='green')
    axes[0, 1].set_yticks(range(top_n))
    axes[0, 1].set_yticklabels([f"#{i+1}" for i in range(top_n)])
    axes[0, 1].set_xlabel('Number of Whistles')
    axes[0, 1].set_title('Whistle Count')
    axes[0, 1].invert_yaxis()
    axes[0, 1].grid(True, alpha=0.3, axis='x')
    
    # 3. Whistle coverage
    axes[1, 0].barh(range(top_n), coverage, color='orange')
    axes[1, 0].set_yticks(range(top_n))
    axes[1, 0].set_yticklabels([f"#{i+1}" for i in range(top_n)])
    axes[1, 0].set_xlabel('Whistle Coverage (%)')
    axes[1, 0].set_title('Temporal Coverage')
    axes[1, 0].invert_yaxis()
    axes[1, 0].grid(True, alpha=0.3, axis='x')
    
    # 4. Score vs Whistles scatter
    axes[1, 1].scatter(whistles, scores, s=100, alpha=0.6, c=coverage, cmap='viridis')
    axes[1, 1].set_xlabel('Number of Whistles')
    axes[1, 1].set_ylabel('Interestingness Score')
    axes[1, 1].set_title('Score vs Whistle Count')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(axes[1, 1].collections[0], ax=axes[1, 1])
    cbar.set_label('Coverage (%)')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def generate_detailed_report(results: list, output_path: Path):
    """Generate detailed markdown report with rankings and stats."""
    results = sorted(results, key=lambda x: x.get('interestingness_score', 0), reverse=True)
    
    with open(output_path, 'w') as f:
        f.write("# Interesting EARS Files - Detailed Report\n\n")
        f.write(f"Generated: {Path.cwd()}\n\n")
        f.write("---\n\n")
        
        f.write("## Top 20 Most Interesting Files\n\n")
        f.write("Ranked by overall interestingness score (combination of whistle activity, ")
        f.write("signal quality, coverage, and spectral characteristics).\n\n")
        
        f.write("| Rank | Score | Whistles | Coverage | Duration | File |\n")
        f.write("|------|-------|----------|----------|----------|------|\n")
        
        for i, result in enumerate(results[:20], 1):
            score = result.get('interestingness_score', 0)
            whistles = result.get('n_whistles', 0)
            coverage = result.get('whistle_coverage_percent', 0)
            duration = result.get('duration', 0)
            filename = Path(result['file']).name
            
            f.write(f"| {i} | {score:.1f} | {whistles} | {coverage:.1f}% | {duration:.2f}s | `{filename}` |\n")
        
        f.write("\n## Score Distribution\n\n")
        
        # Calculate statistics
        scores = [r.get('interestingness_score', 0) for r in results]
        whistles = [r.get('n_whistles', 0) for r in results]
        
        f.write(f"- **Total files analyzed**: {len(results)}\n")
        f.write(f"- **Mean score**: {np.mean(scores):.2f}\n")
        f.write(f"- **Median score**: {np.median(scores):.2f}\n")
        f.write(f"- **Top score**: {max(scores):.2f}\n")
        f.write(f"- **Mean whistles**: {np.mean(whistles):.2f}\n")
        f.write(f"- **Max whistles**: {max(whistles)}\n")
        
        f.write("\n## Recommendations\n\n")
        f.write("### Best for Publication/Presentation\n")
        f.write("Files with highest scores and clear whistle activity:\n\n")
        
        for i, result in enumerate(results[:5], 1):
            filename = Path(result['file']).name
            score = result.get('interestingness_score', 0)
            whistles = result.get('n_whistles', 0)
            f.write(f"{i}. **{filename}** - Score: {score:.1f}, Whistles: {whistles}\n")
        
        f.write("\n### Best for Whistle Analysis\n")
        f.write("Files with highest whistle counts:\n\n")
        
        whistle_sorted = sorted(results, key=lambda x: x.get('n_whistles', 0), reverse=True)
        for i, result in enumerate(whistle_sorted[:5], 1):
            filename = Path(result['file']).name
            whistles = result.get('n_whistles', 0)
            coverage = result.get('whistle_coverage_percent', 0)
            f.write(f"{i}. **{filename}** - Whistles: {whistles}, Coverage: {coverage:.1f}%\n")


def main():
    parser = argparse.ArgumentParser(description='Explore interesting EARS files')
    parser.add_argument('--results', type=Path, required=True,
                       help='Path to interesting_files.json')
    parser.add_argument('--top', type=int, default=10,
                       help='Number of top files to visualize in detail (default: 10)')
    parser.add_argument('--output-dir', type=Path,
                       help='Output directory (default: interesting_files_analysis/visualizations)')
    
    args = parser.parse_args()
    
    # Load results
    print(f"Loading results from {args.results}...")
    with open(args.results, 'r') as f:
        data = json.load(f)
    
    # Get stage 3 results (most detailed)
    results = data.get('stage3_summary', {}).get('results', [])
    
    if not results:
        print("No results found in file!")
        return
    
    print(f"Found {len(results)} analyzed files")
    
    # Set output directory
    output_dir = args.output_dir or (args.results.parent / "visualizations")
    output_dir.mkdir(exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Create comparison plot
    print("\nCreating comparison plot...")
    create_comparison_plot(results, output_dir / "top_files_comparison.png")
    print(f"✓ Saved: {output_dir / 'top_files_comparison.png'}")
    
    # Create detailed plots for top N files
    print(f"\nCreating detailed visualizations for top {args.top} files...")
    
    # Sort by score
    results_sorted = sorted(results, key=lambda x: x.get('interestingness_score', 0), reverse=True)
    
    for i, result in enumerate(results_sorted[:args.top], 1):
        file_path = Path(result['file'])
        
        if not file_path.exists():
            print(f"  ⚠️  File not found: {file_path.name}")
            continue
        
        output_path = output_dir / f"rank{i:02d}_{file_path.stem}.png"
        
        print(f"  [{i}/{args.top}] {file_path.name}...")
        try:
            create_detailed_plot(file_path, output_path)
            print(f"      ✓ Saved: {output_path.name}")
        except Exception as e:
            print(f"      ⚠️  Error: {e}")
    
    # Generate detailed report
    print("\nGenerating detailed report...")
    report_path = output_dir / "detailed_report.md"
    generate_detailed_report(results, report_path)
    print(f"✓ Saved: {report_path}")
    
    print("\n" + "="*80)
    print("✅ EXPLORATION COMPLETE!")
    print("="*80)
    print(f"\nResults in: {output_dir}/")
    print(f"  - top_files_comparison.png (overview)")
    print(f"  - rank01_*.png through rank{args.top:02d}_*.png (detailed plots)")
    print(f"  - detailed_report.md (markdown report)")


if __name__ == '__main__':
    main()
