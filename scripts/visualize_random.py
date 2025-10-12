#!/usr/bin/env python3
"""
Visualize random EARS files for sanity checking.

Creates detailed plots for any files - great for spot-checking data quality.

Usage:
    python visualize_random.py --file-list ears_files_list.txt --n-files 5
    python visualize_random.py --files /path/to/file1.210 /path/to/file2.210
"""

import sys
import argparse
import random
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


def create_detailed_plot(file_path: Path, output_path: Path = None, rank: int = None):
    """
    Create comprehensive visualization of a single file.
    
    Shows:
    - Waveform (raw and denoised)
    - Spectrogram
    - Whistle detections overlaid
    - Power spectral density
    """
    print(f"  Processing: {file_path.name}")
    
    try:
        # Read data
        data = dolphain.read_ears_file(file_path)
        signal = data['data']
        sample_rate = data['fs']  # EARS files use 'fs' not 'sample_rate'
        duration = data['duration']
        
        # Process
        signal_clean = dolphain.wavelet_denoise(signal, wavelet='db8')
        whistles = dolphain.detect_whistles(
            signal_clean,
            fs=sample_rate,  # Parameter is 'fs' not 'sample_rate'
            power_threshold_percentile=85.0,
            min_duration=0.1
        )
        
        # Calculate SNR
        noise = signal - signal_clean
        snr = 10 * np.log10(
            np.mean(signal_clean ** 2) / (np.mean(noise ** 2) + 1e-10)
        )
        
        # Create figure
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.3)
        
        # Title
        title = f"{file_path.name}"
        if rank is not None:
            title = f"Sample #{rank} - {title}"
        title += f"\nDuration: {duration:.2f}s | Whistles: {len(whistles)} | "
        title += f"SNR: {snr:.1f} dB"
        if whistles:
            coverage = sum(w['duration'] for w in whistles) / duration * 100
            title += f" | Coverage: {coverage:.1f}%"
        
        fig.suptitle(title, fontsize=13, fontweight='bold')
        
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
        for i, whistle in enumerate(whistles):
            start_time = whistle['start_time']
            end_time = whistle['end_time']
            label = 'Whistle' if i == 0 else ''
            ax2.axvspan(start_time, end_time, alpha=0.3, color='red', label=label)
        
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Amplitude')
        ax2.set_title(f'Denoised Waveform with Whistle Detections (n={len(whistles)})')
        ax2.grid(True, alpha=0.3)
        if whistles:
            ax2.legend()
        
        # 3. Spectrogram
        ax3 = fig.add_subplot(gs[2, :])
        
        # Calculate spectrogram
        from scipy import signal as scipy_signal
        nperseg = min(2048, len(signal_clean) // 8)
        f, t, Sxx = scipy_signal.spectrogram(
            signal_clean,
            fs=sample_rate,
            nperseg=nperseg,
            noverlap=nperseg // 2
        )
        
        # Plot
        im = ax3.pcolormesh(t, f / 1000, 10 * np.log10(Sxx + 1e-10),
                           shading='gouraud', cmap='viridis')
        
        # Overlay whistle detections
        for whistle in whistles:
            start_time = whistle['start_time']
            end_time = whistle['end_time']
            ax3.axvline(start_time, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
            ax3.axvline(end_time, color='red', linestyle='--', alpha=0.7, linewidth=1.5)
        
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Frequency (kHz)')
        ax3.set_title('Spectrogram (Denoised)')
        ax3.set_ylim([0, min(50, sample_rate / 2000)])
        
        # Add colorbar
        plt.colorbar(im, ax=ax3, label='Power (dB)')
        
        # Save or show
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            print(f"    ✓ Saved: {output_path.name}")
        else:
            plt.show()
        
        return True
        
    except Exception as e:
        print(f"    ⚠️  Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Visualize random EARS files for sanity checking',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Visualize 5 random files
  python visualize_random.py --file-list ears_files_list.txt --n-files 5
  
  # Visualize specific files
  python visualize_random.py --files /path/to/file1.210 /path/to/file2.210
  
  # Sample from results CSV
  python visualize_random.py --from-results quick_find_results/all_results.csv --n-files 5
        """
    )
    
    parser.add_argument('--file-list', type=Path,
                       help='File list to sample from')
    parser.add_argument('--files', type=Path, nargs='+',
                       help='Specific files to visualize')
    parser.add_argument('--from-results', type=Path,
                       help='Sample from results CSV file')
    parser.add_argument('--n-files', type=int, default=5,
                       help='Number of random files to visualize (default: 5)')
    parser.add_argument('--output-dir', type=Path, default=Path('sanity_check_plots'),
                       help='Output directory (default: sanity_check_plots)')
    
    args = parser.parse_args()
    
    # Create output directory
    args.output_dir.mkdir(exist_ok=True)
    
    # Get file list
    files_to_plot = []
    
    if args.files:
        # Specific files provided
        files_to_plot = args.files
        print(f"Visualizing {len(files_to_plot)} specific files...")
        
    elif args.from_results:
        # Sample from results CSV
        print(f"Loading results from: {args.from_results}")
        import pandas as pd
        df = pd.read_csv(args.from_results)
        
        # Sample randomly
        if len(df) > args.n_files:
            df_sample = df.sample(n=args.n_files, random_state=42)
        else:
            df_sample = df
        
        files_to_plot = [Path(f) for f in df_sample['file']]
        print(f"Sampled {len(files_to_plot)} random files from results")
        
    elif args.file_list:
        # Sample from file list
        print(f"Loading file list from: {args.file_list}")
        with open(args.file_list, 'r') as f:
            all_files = [Path(line.strip()) for line in f if line.strip()]
        
        print(f"Loaded {len(all_files)} files")
        
        # Sample randomly
        if len(all_files) > args.n_files:
            files_to_plot = random.sample(all_files, args.n_files)
        else:
            files_to_plot = all_files
        
        print(f"Randomly sampled {len(files_to_plot)} files")
        
    else:
        print("❌ Error: Must provide --file-list, --files, or --from-results")
        parser.print_help()
        sys.exit(1)
    
    # Validate files exist
    valid_files = []
    for f in files_to_plot:
        if f.exists():
            valid_files.append(f)
        else:
            print(f"⚠️  File not found: {f}")
    
    if not valid_files:
        print("❌ No valid files to plot!")
        sys.exit(1)
    
    print(f"\n{'='*80}")
    print(f"Creating visualizations for {len(valid_files)} files...")
    print(f"{'='*80}\n")
    
    # Create plots
    success_count = 0
    for i, file_path in enumerate(valid_files, 1):
        output_path = args.output_dir / f"sample_{i:02d}_{file_path.stem}.png"
        
        print(f"[{i}/{len(valid_files)}]")
        if create_detailed_plot(file_path, output_path, rank=i):
            success_count += 1
    
    print(f"\n{'='*80}")
    print(f"✅ COMPLETE!")
    print(f"{'='*80}")
    print(f"Successfully created {success_count}/{len(valid_files)} plots")
    print(f"Saved to: {args.output_dir}/")
    print(f"\nFiles:")
    for i in range(1, success_count + 1):
        png_file = args.output_dir / f"sample_{i:02d}_*.png"
        print(f"  {i}. {png_file}")


if __name__ == '__main__':
    main()
