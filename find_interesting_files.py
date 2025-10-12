#!/usr/bin/env python3
"""
Find interesting EARS files with high-quality dolphin acoustic activity.

"Interesting" files are those with:
1. High whistle activity (lots of vocalizations)
2. Good signal quality (high SNR, clear signals)
3. Diverse acoustic features (multiple whistle types, frequency patterns)
4. Minimal noise/artifacts
5. High energy in whistle frequency bands (5-25 kHz)

Usage:
    python find_interesting_files.py --catalog data_drive_catalog.json
    python find_interesting_files.py --catalog data_drive_catalog.json --resume
    python find_interesting_files.py --quick  # Quick scan mode
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import numpy as np

# Add dolphain to path if needed
sys.path.insert(0, str(Path(__file__).parent))

import dolphain


class InterestingFileFinder:
    """
    Multi-stage pipeline to identify the most interesting acoustic files.
    
    Stage 1: Quick Scan - Fast metrics on all files (RMS, spectral features)
    Stage 2: Whistle Detection - Full analysis on promising candidates
    Stage 3: Deep Analysis - Detailed characterization of top files
    """
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("interesting_files_analysis")
        self.output_dir.mkdir(exist_ok=True)
        
        # Results storage
        self.stage1_results = []  # Quick scan results
        self.stage2_results = []  # Whistle detection results
        self.stage3_results = []  # Deep analysis results
        
        # Progress tracking
        self.progress_file = self.output_dir / "progress.json"
        self.processed_files = set()
        
        print(f"✓ Output directory: {self.output_dir}")
    
    def load_progress(self) -> bool:
        """Load progress from previous run."""
        if not self.progress_file.exists():
            return False
        
        try:
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
                self.processed_files = set(data.get('processed_files', []))
                self.stage1_results = data.get('stage1_results', [])
                self.stage2_results = data.get('stage2_results', [])
                self.stage3_results = data.get('stage3_results', [])
                print(f"✓ Resumed: {len(self.processed_files)} files already processed")
                return True
        except Exception as e:
            print(f"⚠️  Could not load progress: {e}")
            return False
    
    def save_progress(self):
        """Save current progress."""
        try:
            data = {
                'processed_files': list(self.processed_files),
                'stage1_results': self.stage1_results,
                'stage2_results': self.stage2_results,
                'stage3_results': self.stage3_results,
                'last_update': datetime.now().isoformat()
            }
            with open(self.progress_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving progress: {e}")
    
    def calculate_interestingness_score(self, metrics: Dict) -> float:
        """
        Calculate overall interestingness score (0-100).
        
        Higher scores = more interesting for dolphin research.
        """
        score = 0.0
        
        # Whistle activity (0-40 points)
        n_whistles = metrics.get('n_whistles', 0)
        if n_whistles > 0:
            score += min(40, n_whistles * 0.5)  # Cap at 40 points
        
        # Signal quality (0-20 points)
        snr = metrics.get('snr_db', 0)
        if snr > 5:
            score += min(20, (snr - 5) * 2)  # Cap at 20 points
        
        # Whistle coverage (0-15 points)
        coverage = metrics.get('whistle_coverage_percent', 0)
        score += min(15, coverage * 0.15)
        
        # Whistle band energy (0-15 points)
        whistle_power = metrics.get('whistle_band_power_pct', 0)
        score += min(15, whistle_power * 0.15)
        
        # Diversity/complexity (0-10 points)
        spectral_spread = metrics.get('spectral_bandwidth', 0)
        if spectral_spread > 5000:  # Wide frequency range
            score += min(10, (spectral_spread - 5000) / 1000)
        
        return round(score, 2)
    
    def stage1_quick_scan(self, file_path: Path) -> Dict:
        """
        Stage 1: Quick scan for basic quality metrics.
        Fast analysis to filter out obviously bad files.
        """
        try:
            # Read file
            data = dolphain.read_ears_file(file_path)
            signal = data['data']
            sample_rate = data['sample_rate']
            
            # Basic metrics
            rms = float(np.sqrt(np.mean(signal ** 2)))
            peak = float(np.max(np.abs(signal)))
            
            # Quick spectral analysis
            from scipy import signal as scipy_signal
            freqs, psd = scipy_signal.welch(signal, fs=sample_rate, nperseg=2048)
            
            # Energy in whistle bands (5-25 kHz)
            whistle_mask = (freqs >= 5000) & (freqs <= 25000)
            whistle_power = float(np.sum(psd[whistle_mask]))
            total_power = float(np.sum(psd))
            whistle_power_pct = (whistle_power / total_power * 100) if total_power > 0 else 0
            
            # Spectral centroid (weighted mean frequency)
            spectral_centroid = float(np.sum(freqs * psd) / np.sum(psd)) if np.sum(psd) > 0 else 0
            
            # Spectral bandwidth
            spectral_bandwidth = float(np.sqrt(np.sum(((freqs - spectral_centroid) ** 2) * psd) / np.sum(psd)))
            
            return {
                'file': str(file_path),
                'duration': data['duration'],
                'rms': rms,
                'peak': peak,
                'whistle_band_power_pct': whistle_power_pct,
                'spectral_centroid': spectral_centroid,
                'spectral_bandwidth': spectral_bandwidth,
                'stage': 1,
                'error': None
            }
            
        except Exception as e:
            return {
                'file': str(file_path),
                'stage': 1,
                'error': str(e)
            }
    
    def stage2_whistle_detection(self, file_path: Path) -> Dict:
        """
        Stage 2: Full whistle detection on promising files.
        """
        try:
            # Use our proven pipeline
            pipeline = dolphain.WhistleDetectionPipeline(
                denoise=True,
                power_threshold_percentile=85.0,
                min_duration=0.1
            )
            
            result = pipeline(file_path)
            result['stage'] = 2
            result['error'] = None
            
            # Add SNR estimate
            data = dolphain.read_ears_file(file_path)
            signal = data['data']
            signal_clean = dolphain.wavelet_denoise(signal, wavelet='db8')
            noise = signal - signal_clean
            snr = 10 * np.log10(
                np.mean(signal_clean ** 2) / (np.mean(noise ** 2) + 1e-10)
            )
            result['snr_db'] = float(snr)
            
            return result
            
        except Exception as e:
            return {
                'file': str(file_path),
                'stage': 2,
                'error': str(e)
            }
    
    def stage3_deep_analysis(self, file_path: Path) -> Dict:
        """
        Stage 3: Deep characterization of top files.
        """
        try:
            # Full spectral + temporal analysis
            data = dolphain.read_ears_file(file_path)
            signal = data['data']
            sample_rate = data['sample_rate']
            
            # Denoise
            signal_clean = dolphain.wavelet_denoise(signal, wavelet='db8')
            
            # Whistle detection
            whistles = dolphain.detect_whistles(
                signal_clean,
                sample_rate=sample_rate,
                power_threshold_percentile=85.0,
                min_duration=0.1
            )
            
            # Detailed spectral analysis
            bands = {
                'low': (0, 5000),
                'whistle_low': (5000, 15000),
                'whistle_high': (15000, 25000),
                'ultrasonic': (25000, 100000),
            }
            
            from scipy import signal as scipy_signal
            freqs, psd = scipy_signal.welch(signal_clean, fs=sample_rate, nperseg=4096)
            
            band_powers = {}
            for band_name, (f_low, f_high) in bands.items():
                mask = (freqs >= f_low) & (freqs <= f_high)
                band_powers[f'{band_name}_power'] = float(np.sum(psd[mask]))
            
            # Temporal segmentation (find active regions)
            window_size = int(sample_rate * 0.5)  # 0.5s windows
            n_windows = len(signal_clean) // window_size
            window_energies = []
            
            for i in range(n_windows):
                start = i * window_size
                end = start + window_size
                window = signal_clean[start:end]
                energy = np.sum(window ** 2)
                window_energies.append(energy)
            
            # Find high-energy segments
            if len(window_energies) > 0:
                energy_threshold = np.percentile(window_energies, 75)
                active_windows = sum(1 for e in window_energies if e > energy_threshold)
                activity_ratio = active_windows / len(window_energies)
            else:
                activity_ratio = 0
            
            return {
                'file': str(file_path),
                'duration': data['duration'],
                'n_whistles': len(whistles),
                'mean_whistle_duration': float(np.mean([w['duration'] for w in whistles])) if whistles else 0,
                'whistle_coverage_percent': sum(w['duration'] for w in whistles) / data['duration'] * 100 if data['duration'] > 0 else 0,
                **band_powers,
                'activity_ratio': float(activity_ratio),
                'n_active_segments': int(active_windows) if 'active_windows' in locals() else 0,
                'stage': 3,
                'error': None
            }
            
        except Exception as e:
            return {
                'file': str(file_path),
                'stage': 3,
                'error': str(e)
            }
    
    def run_stage1(self, file_paths: List[Path], sample_rate: float = 0.1) -> List[Path]:
        """
        Run Stage 1 quick scan on files.
        
        Args:
            file_paths: List of files to scan
            sample_rate: Fraction of files to sample (0-1)
        
        Returns:
            Promising files for Stage 2
        """
        print(f"\n{'='*80}")
        print(f"STAGE 1: Quick Scan")
        print(f"{'='*80}")
        
        # Sample files if requested
        if sample_rate < 1.0:
            import random
            n_sample = max(1, int(len(file_paths) * sample_rate))
            file_paths = random.sample(file_paths, n_sample)
            print(f"Sampling {n_sample} of {len(file_paths)} files ({sample_rate*100:.1f}%)")
        
        print(f"Scanning {len(file_paths)} files...")
        
        processed = 0
        for i, file_path in enumerate(file_paths):
            if str(file_path) in self.processed_files:
                continue
            
            result = self.stage1_quick_scan(file_path)
            self.stage1_results.append(result)
            self.processed_files.add(str(file_path))
            processed += 1
            
            # Progress update
            if (i + 1) % 100 == 0:
                print(f"  Progress: {i+1}/{len(file_paths)} files", flush=True)
                self.save_progress()
        
        # Save final results
        self.save_progress()
        
        # Filter for promising files
        # Criteria: High whistle band power (>20%) AND reasonable signal level
        promising = []
        for result in self.stage1_results:
            if result.get('error'):
                continue
            
            whistle_power = result.get('whistle_band_power_pct', 0)
            rms = result.get('rms', 0)
            
            if whistle_power > 20 and rms > 0.01:  # Thresholds based on experience
                promising.append(Path(result['file']))
        
        print(f"\n✓ Stage 1 complete: {processed} files processed")
        print(f"  Found {len(promising)} promising files ({len(promising)/max(len(file_paths),1)*100:.1f}%)")
        
        return promising
    
    def run_stage2(self, file_paths: List[Path]) -> List[Path]:
        """
        Run Stage 2 whistle detection on promising files.
        
        Returns:
            Top files for Stage 3
        """
        print(f"\n{'='*80}")
        print(f"STAGE 2: Whistle Detection")
        print(f"{'='*80}")
        print(f"Analyzing {len(file_paths)} promising files...")
        
        for i, file_path in enumerate(file_paths):
            result = self.stage2_whistle_detection(file_path)
            self.stage2_results.append(result)
            
            # Progress update
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(file_paths)} files", flush=True)
                self.save_progress()
        
        # Save final results
        self.save_progress()
        
        # Calculate interestingness scores
        scored_results = []
        for result in self.stage2_results:
            if result.get('error'):
                continue
            
            score = self.calculate_interestingness_score(result)
            result['interestingness_score'] = score
            scored_results.append(result)
        
        # Sort by score
        scored_results.sort(key=lambda x: x['interestingness_score'], reverse=True)
        
        # Take top 10% or at least 20 files
        n_top = max(20, int(len(scored_results) * 0.1))
        top_files = [Path(r['file']) for r in scored_results[:n_top]]
        
        print(f"\n✓ Stage 2 complete: {len(file_paths)} files analyzed")
        print(f"  Found {len(scored_results)} valid results")
        print(f"  Selected top {len(top_files)} for deep analysis")
        if scored_results:
            print(f"  Top score: {scored_results[0]['interestingness_score']:.1f}/100")
        
        return top_files
    
    def run_stage3(self, file_paths: List[Path]):
        """
        Run Stage 3 deep analysis on top files.
        """
        print(f"\n{'='*80}")
        print(f"STAGE 3: Deep Analysis")
        print(f"{'='*80}")
        print(f"Deep analysis of {len(file_paths)} top files...")
        
        for i, file_path in enumerate(file_paths):
            print(f"  [{i+1}/{len(file_paths)}] {file_path.name}", flush=True)
            result = self.stage3_deep_analysis(file_path)
            
            # Calculate final score
            result['interestingness_score'] = self.calculate_interestingness_score(result)
            self.stage3_results.append(result)
            
            self.save_progress()
        
        # Sort by final score
        self.stage3_results.sort(key=lambda x: x.get('interestingness_score', 0), reverse=True)
        
        print(f"\n✓ Stage 3 complete: {len(file_paths)} files deeply analyzed")
    
    def generate_report(self):
        """Generate final report of interesting files."""
        report_path = self.output_dir / "interesting_files_report.txt"
        json_path = self.output_dir / "interesting_files.json"
        
        with open(report_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("INTERESTING FILES REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Stage 1 summary
            f.write("STAGE 1: Quick Scan\n")
            f.write("-"*80 + "\n")
            f.write(f"Files scanned: {len(self.stage1_results)}\n")
            if self.stage1_results:
                valid = [r for r in self.stage1_results if not r.get('error')]
                f.write(f"Valid results: {len(valid)}\n")
                if valid:
                    mean_whistle_power = np.mean([r['whistle_band_power_pct'] for r in valid])
                    f.write(f"Mean whistle band power: {mean_whistle_power:.1f}%\n")
            f.write("\n")
            
            # Stage 2 summary
            f.write("STAGE 2: Whistle Detection\n")
            f.write("-"*80 + "\n")
            f.write(f"Files analyzed: {len(self.stage2_results)}\n")
            if self.stage2_results:
                valid = [r for r in self.stage2_results if not r.get('error')]
                f.write(f"Valid results: {len(valid)}\n")
                if valid:
                    mean_whistles = np.mean([r.get('n_whistles', 0) for r in valid])
                    f.write(f"Mean whistles detected: {mean_whistles:.1f}\n")
            f.write("\n")
            
            # Stage 3 summary
            f.write("STAGE 3: Deep Analysis\n")
            f.write("-"*80 + "\n")
            f.write(f"Files deeply analyzed: {len(self.stage3_results)}\n\n")
            
            # Top 20 most interesting files
            f.write("TOP 20 MOST INTERESTING FILES\n")
            f.write("-"*80 + "\n")
            f.write(f"{'Rank':<6} {'Score':<8} {'Whistles':<10} {'Coverage':<10} {'File'}\n")
            f.write("-"*80 + "\n")
            
            for i, result in enumerate(self.stage3_results[:20], 1):
                score = result.get('interestingness_score', 0)
                n_whistles = result.get('n_whistles', 0)
                coverage = result.get('whistle_coverage_percent', 0)
                filename = Path(result['file']).name
                
                f.write(f"{i:<6} {score:<8.1f} {n_whistles:<10} {coverage:<9.1f}% {filename}\n")
        
        # Save detailed JSON
        output_data = {
            'stage1_summary': {
                'n_scanned': len(self.stage1_results),
                'results': self.stage1_results
            },
            'stage2_summary': {
                'n_analyzed': len(self.stage2_results),
                'results': self.stage2_results
            },
            'stage3_summary': {
                'n_deep_analyzed': len(self.stage3_results),
                'results': self.stage3_results
            },
            'top_files': self.stage3_results[:20]
        }
        
        with open(json_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n✓ Reports saved:")
        print(f"  {report_path}")
        print(f"  {json_path}")


def main():
    parser = argparse.ArgumentParser(description='Find interesting EARS files')
    parser.add_argument('--catalog', type=Path, help='Path to data_drive_catalog.json')
    parser.add_argument('--data-dir', type=Path, help='Direct path to data directory')
    parser.add_argument('--resume', action='store_true', help='Resume from checkpoint')
    parser.add_argument('--quick', action='store_true', help='Quick mode (sample 10% of files)')
    parser.add_argument('--sample-rate', type=float, default=0.1, 
                       help='Fraction of files to sample in Stage 1 (0-1, default 0.1)')
    
    args = parser.parse_args()
    
    # Get file list
    file_paths = []
    
    if args.catalog:
        print(f"Loading catalog from {args.catalog}...")
        with open(args.catalog, 'r') as f:
            catalog = json.load(f)
        
        # Extract EARS files from catalog
        root_dir = Path(catalog['root_directory'])
        for dir_path, stats in catalog['catalog'].items():
            if stats['ears_files'] > 0:
                # Would need to actually list files - catalog only has counts
                # This is a limitation - we need actual file lists
                pass
        
        if not file_paths:
            print("⚠️  Catalog doesn't contain file lists, only statistics.")
            print("   Use --data-dir instead to scan directly.")
            sys.exit(1)
    
    elif args.data_dir:
        print(f"Finding EARS files in {args.data_dir}...")
        file_paths = dolphain.find_data_files(args.data_dir, '**/*.[0-9][0-9][0-9]')
        print(f"Found {len(file_paths)} EARS files")
    
    else:
        print("Error: Must specify either --catalog or --data-dir")
        parser.print_help()
        sys.exit(1)
    
    if not file_paths:
        print("No files found!")
        sys.exit(1)
    
    # Set sample rate for quick mode
    if args.quick:
        args.sample_rate = 0.1
    
    # Run analysis
    finder = InterestingFileFinder()
    
    if args.resume:
        finder.load_progress()
    
    try:
        # Stage 1: Quick scan
        promising_files = finder.run_stage1(file_paths, sample_rate=args.sample_rate)
        
        # Stage 2: Whistle detection
        top_files = finder.run_stage2(promising_files)
        
        # Stage 3: Deep analysis
        finder.run_stage3(top_files)
        
        # Generate report
        finder.generate_report()
        
        print("\n" + "="*80)
        print("✅ ANALYSIS COMPLETE!")
        print("="*80)
        print(f"\nTop file: {Path(finder.stage3_results[0]['file']).name}")
        print(f"Score: {finder.stage3_results[0]['interestingness_score']:.1f}/100")
        print(f"Whistles: {finder.stage3_results[0]['n_whistles']}")
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
        finder.save_progress()
        print("Progress saved. Resume with --resume flag.")


if __name__ == '__main__':
    main()
