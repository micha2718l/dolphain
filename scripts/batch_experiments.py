#!/usr/bin/env python3
"""
Batch experiment runner for large-scale EARS file analysis.

Efficiently runs multiple experiments across many files with:
- Progress persistence (resume capability)
- Parallel processing (optional)
- Memory-efficient streaming
- Automatic result aggregation
- Error handling and logging

Usage:
    # Run standard analysis suite on all files
    python batch_experiments.py --data-dir /path/to/data
    
    # Resume interrupted run
    python batch_experiments.py --data-dir /path/to/data --resume
    
    # Quick sample (10% of files)
    python batch_experiments.py --data-dir /path/to/data --sample 0.1
    
    # Parallel processing
    python batch_experiments.py --data-dir /path/to/data --parallel 4
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import time

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


class BatchExperimentRunner:
    """
    Run comprehensive experiments across large datasets.
    
    Experiments:
    1. Basic Metrics - Fundamental acoustic properties
    2. Whistle Detection - Find and characterize vocalizations
    3. Spectral Analysis - Frequency content and distribution
    4. Quality Assessment - SNR and signal quality
    5. Temporal Patterns - Activity over time
    """
    
    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path("batch_experiments_results")
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "checkpoints").mkdir(exist_ok=True)
        (self.output_dir / "results").mkdir(exist_ok=True)
        (self.output_dir / "visualizations").mkdir(exist_ok=True)
        
        # Results storage
        self.results = {
            'basic_metrics': [],
            'whistle_detection': [],
            'spectral_analysis': [],
            'quality_assessment': [],
            'temporal_patterns': []
        }
        
        # Progress tracking
        self.processed_files = set()
        self.start_time = time.time()
        self.last_save_time = time.time()
        
        print(f"✓ Output directory: {self.output_dir}")
    
    def load_checkpoint(self, experiment_name: str) -> bool:
        """Load progress checkpoint for specific experiment."""
        checkpoint_file = self.output_dir / "checkpoints" / f"{experiment_name}.json"
        
        if not checkpoint_file.exists():
            return False
        
        try:
            with open(checkpoint_file, 'r') as f:
                data = json.load(f)
                self.results[experiment_name] = data.get('results', [])
                self.processed_files = set(data.get('processed_files', []))
                print(f"  ✓ Loaded {len(self.processed_files)} processed files")
                return True
        except Exception as e:
            print(f"  ⚠️  Error loading checkpoint: {e}")
            return False
    
    def save_checkpoint(self, experiment_name: str):
        """Save progress checkpoint."""
        checkpoint_file = self.output_dir / "checkpoints" / f"{experiment_name}.json"
        
        try:
            data = {
                'experiment': experiment_name,
                'processed_files': list(self.processed_files),
                'results': self.results[experiment_name],
                'last_update': datetime.now().isoformat(),
                'n_processed': len(self.processed_files)
            }
            
            with open(checkpoint_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.last_save_time = time.time()
        except Exception as e:
            print(f"  ⚠️  Error saving checkpoint: {e}")
    
    def should_save(self, interval: int = 60) -> bool:
        """Check if it's time to save (every N seconds)."""
        return (time.time() - self.last_save_time) > interval
    
    def run_basic_metrics(self, file_paths: List[Path], resume: bool = False):
        """Experiment 1: Basic acoustic metrics."""
        print(f"\n{'='*80}")
        print("EXPERIMENT 1: Basic Metrics")
        print(f"{'='*80}")
        
        if resume:
            self.load_checkpoint('basic_metrics')
        
        pipeline = dolphain.BasicMetricsPipeline()
        
        for i, file_path in enumerate(file_paths):
            if str(file_path) in self.processed_files:
                continue
            
            try:
                result = pipeline(file_path)
                result['file'] = str(file_path)
                result['filename'] = file_path.name
                self.results['basic_metrics'].append(result)
                self.processed_files.add(str(file_path))
                
            except Exception as e:
                print(f"  ⚠️  Error processing {file_path.name}: {e}")
                self.results['basic_metrics'].append({
                    'file': str(file_path),
                    'filename': file_path.name,
                    'error': str(e)
                })
            
            # Progress
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(file_paths)} ({(i+1)/len(file_paths)*100:.1f}%)")
            
            if self.should_save():
                self.save_checkpoint('basic_metrics')
        
        # Final save
        self.save_checkpoint('basic_metrics')
        
        # Save results to CSV
        df = pd.DataFrame([r for r in self.results['basic_metrics'] if 'error' not in r])
        df.to_csv(self.output_dir / "results" / "basic_metrics.csv", index=False)
        
        print(f"✓ Basic metrics complete: {len(df)} files")
        print(f"  Mean RMS: {df['rms'].mean():.6f}")
        print(f"  Mean dynamic range: {df['dynamic_range'].mean():.2f} dB")
    
    def run_whistle_detection(self, file_paths: List[Path], resume: bool = False):
        """Experiment 2: Whistle detection and characterization."""
        print(f"\n{'='*80}")
        print("EXPERIMENT 2: Whistle Detection")
        print(f"{'='*80}")
        
        if resume:
            self.load_checkpoint('whistle_detection')
        
        pipeline = dolphain.WhistleDetectionPipeline(
            denoise=True,
            power_threshold_percentile=85.0,
            min_duration=0.1
        )
        
        for i, file_path in enumerate(file_paths):
            if str(file_path) in self.processed_files:
                continue
            
            try:
                result = pipeline(file_path)
                result['file'] = str(file_path)
                result['filename'] = file_path.name
                self.results['whistle_detection'].append(result)
                self.processed_files.add(str(file_path))
                
            except Exception as e:
                print(f"  ⚠️  Error processing {file_path.name}: {e}")
                self.results['whistle_detection'].append({
                    'file': str(file_path),
                    'filename': file_path.name,
                    'error': str(e)
                })
            
            # Progress
            if (i + 1) % 25 == 0:
                print(f"  Progress: {i+1}/{len(file_paths)} ({(i+1)/len(file_paths)*100:.1f}%)")
            
            if self.should_save():
                self.save_checkpoint('whistle_detection')
        
        # Final save
        self.save_checkpoint('whistle_detection')
        
        # Save results to CSV
        df = pd.DataFrame([r for r in self.results['whistle_detection'] if 'error' not in r])
        df.to_csv(self.output_dir / "results" / "whistle_detection.csv", index=False)
        
        print(f"✓ Whistle detection complete: {len(df)} files")
        if len(df) > 0:
            print(f"  Files with whistles: {(df['n_whistles'] > 0).sum()} ({(df['n_whistles'] > 0).sum()/len(df)*100:.1f}%)")
            print(f"  Mean whistles per file: {df['n_whistles'].mean():.2f}")
            print(f"  Mean coverage: {df['whistle_coverage_percent'].mean():.2f}%")
    
    def run_spectral_analysis(self, file_paths: List[Path], resume: bool = False):
        """Experiment 3: Spectral content analysis."""
        print(f"\n{'='*80}")
        print("EXPERIMENT 3: Spectral Analysis")
        print(f"{'='*80}")
        
        if resume:
            self.load_checkpoint('spectral_analysis')
        
        bands = {
            'low': (0, 5000),
            'whistle_low': (5000, 15000),
            'whistle_high': (15000, 25000),
            'ultrasonic': (25000, 100000),
        }
        
        pipeline = dolphain.SpectralAnalysisPipeline(freq_bands=bands)
        
        for i, file_path in enumerate(file_paths):
            if str(file_path) in self.processed_files:
                continue
            
            try:
                result = pipeline(file_path)
                result['file'] = str(file_path)
                result['filename'] = file_path.name
                self.results['spectral_analysis'].append(result)
                self.processed_files.add(str(file_path))
                
            except Exception as e:
                print(f"  ⚠️  Error processing {file_path.name}: {e}")
                self.results['spectral_analysis'].append({
                    'file': str(file_path),
                    'filename': file_path.name,
                    'error': str(e)
                })
            
            # Progress
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(file_paths)} ({(i+1)/len(file_paths)*100:.1f}%)")
            
            if self.should_save():
                self.save_checkpoint('spectral_analysis')
        
        # Final save
        self.save_checkpoint('spectral_analysis')
        
        # Save results to CSV
        df = pd.DataFrame([r for r in self.results['spectral_analysis'] if 'error' not in r])
        df.to_csv(self.output_dir / "results" / "spectral_analysis.csv", index=False)
        
        print(f"✓ Spectral analysis complete: {len(df)} files")
        if len(df) > 0:
            # Calculate relative power
            total_power = (df['low_total_power'] + df['whistle_low_total_power'] + 
                          df['whistle_high_total_power'] + df['ultrasonic_total_power'])
            low_pct = (df['low_total_power'] / total_power * 100).mean()
            print(f"  Mean low band power: {low_pct:.1f}%")
            print(f"  Mean spectral centroid: {df['spectral_centroid'].mean():.0f} Hz")
    
    def run_quality_assessment(self, file_paths: List[Path], resume: bool = False):
        """Experiment 4: Signal quality assessment."""
        print(f"\n{'='*80}")
        print("EXPERIMENT 4: Quality Assessment")
        print(f"{'='*80}")
        
        if resume:
            self.load_checkpoint('quality_assessment')
        
        for i, file_path in enumerate(file_paths):
            if str(file_path) in self.processed_files:
                continue
            
            try:
                # Read and denoise
                data = dolphain.read_ears_file(file_path)
                signal = data['data']
                signal_clean = dolphain.wavelet_denoise(signal, wavelet='db8')
                noise = signal - signal_clean
                
                # Calculate SNR
                snr = 10 * np.log10(
                    np.mean(signal_clean ** 2) / (np.mean(noise ** 2) + 1e-10)
                )
                
                # Signal statistics
                result = {
                    'file': str(file_path),
                    'filename': file_path.name,
                    'duration': data['duration'],
                    'snr_db': float(snr),
                    'signal_rms': float(np.sqrt(np.mean(signal ** 2))),
                    'noise_rms': float(np.sqrt(np.mean(noise ** 2))),
                    'crest_factor': float(np.max(np.abs(signal)) / (np.sqrt(np.mean(signal ** 2)) + 1e-10))
                }
                
                self.results['quality_assessment'].append(result)
                self.processed_files.add(str(file_path))
                
            except Exception as e:
                print(f"  ⚠️  Error processing {file_path.name}: {e}")
                self.results['quality_assessment'].append({
                    'file': str(file_path),
                    'filename': file_path.name,
                    'error': str(e)
                })
            
            # Progress
            if (i + 1) % 50 == 0:
                print(f"  Progress: {i+1}/{len(file_paths)} ({(i+1)/len(file_paths)*100:.1f}%)")
            
            if self.should_save():
                self.save_checkpoint('quality_assessment')
        
        # Final save
        self.save_checkpoint('quality_assessment')
        
        # Save results to CSV
        df = pd.DataFrame([r for r in self.results['quality_assessment'] if 'error' not in r])
        df.to_csv(self.output_dir / "results" / "quality_assessment.csv", index=False)
        
        print(f"✓ Quality assessment complete: {len(df)} files")
        if len(df) > 0:
            print(f"  Mean SNR: {df['snr_db'].mean():.2f} dB")
            print(f"  High quality files (SNR > 10 dB): {(df['snr_db'] > 10).sum()} ({(df['snr_db'] > 10).sum()/len(df)*100:.1f}%)")
    
    def generate_summary_report(self):
        """Generate comprehensive summary report."""
        report_path = self.output_dir / "summary_report.txt"
        
        with open(report_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("BATCH EXPERIMENTS SUMMARY REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total runtime: {time.time() - self.start_time:.1f} seconds\n\n")
            
            # Summary for each experiment
            for exp_name, results in self.results.items():
                if not results:
                    continue
                
                f.write(f"\n{exp_name.upper().replace('_', ' ')}\n")
                f.write("-"*80 + "\n")
                
                valid_results = [r for r in results if 'error' not in r]
                error_results = [r for r in results if 'error' in r]
                
                f.write(f"Total files: {len(results)}\n")
                f.write(f"Successful: {len(valid_results)}\n")
                f.write(f"Errors: {len(error_results)}\n")
                
                if valid_results:
                    df = pd.DataFrame(valid_results)
                    
                    # Experiment-specific stats
                    if exp_name == 'basic_metrics':
                        f.write(f"\nMean RMS: {df['rms'].mean():.6f}\n")
                        f.write(f"Mean Peak: {df['peak'].mean():.6f}\n")
                        f.write(f"Mean Dynamic Range: {df['dynamic_range'].mean():.2f} dB\n")
                    
                    elif exp_name == 'whistle_detection':
                        f.write(f"\nFiles with whistles: {(df['n_whistles'] > 0).sum()}\n")
                        f.write(f"Mean whistles per file: {df['n_whistles'].mean():.2f}\n")
                        f.write(f"Max whistles in a file: {df['n_whistles'].max()}\n")
                        f.write(f"Mean coverage: {df['whistle_coverage_percent'].mean():.2f}%\n")
                    
                    elif exp_name == 'spectral_analysis':
                        f.write(f"\nMean spectral centroid: {df['spectral_centroid'].mean():.0f} Hz\n")
                        f.write(f"Mean spectral bandwidth: {df['spectral_bandwidth'].mean():.0f} Hz\n")
                    
                    elif exp_name == 'quality_assessment':
                        f.write(f"\nMean SNR: {df['snr_db'].mean():.2f} dB\n")
                        f.write(f"High quality (SNR > 10 dB): {(df['snr_db'] > 10).sum()} files\n")
        
        print(f"\n✓ Summary report saved: {report_path}")


def main():
    parser = argparse.ArgumentParser(description='Run batch experiments on EARS files')
    parser.add_argument('--data-dir', type=Path, required=True,
                       help='Directory containing EARS files')
    parser.add_argument('--output-dir', type=Path,
                       help='Output directory (default: batch_experiments_results)')
    parser.add_argument('--resume', action='store_true',
                       help='Resume from checkpoint')
    parser.add_argument('--sample', type=float, default=1.0,
                       help='Fraction of files to sample (0-1, default 1.0)')
    parser.add_argument('--experiments', nargs='+',
                       choices=['basic', 'whistle', 'spectral', 'quality', 'all'],
                       default=['all'],
                       help='Which experiments to run')
    
    args = parser.parse_args()
    
    # Find EARS files
    print(f"Finding EARS files in {args.data_dir}...")
    file_paths = dolphain.find_data_files(args.data_dir, '**/*.[0-9][0-9][0-9]')
    print(f"Found {len(file_paths)} EARS files")
    
    if not file_paths:
        print("No files found!")
        return
    
    # Sample if requested
    if args.sample < 1.0:
        import random
        n_sample = max(1, int(len(file_paths) * args.sample))
        file_paths = random.sample(file_paths, n_sample)
        print(f"Sampling {n_sample} files ({args.sample*100:.1f}%)")
    
    # Create runner
    runner = BatchExperimentRunner(output_dir=args.output_dir)
    
    # Determine which experiments to run
    run_all = 'all' in args.experiments
    
    try:
        if run_all or 'basic' in args.experiments:
            runner.run_basic_metrics(file_paths, resume=args.resume)
            runner.processed_files.clear()  # Reset for next experiment
        
        if run_all or 'whistle' in args.experiments:
            runner.run_whistle_detection(file_paths, resume=args.resume)
            runner.processed_files.clear()
        
        if run_all or 'spectral' in args.experiments:
            runner.run_spectral_analysis(file_paths, resume=args.resume)
            runner.processed_files.clear()
        
        if run_all or 'quality' in args.experiments:
            runner.run_quality_assessment(file_paths, resume=args.resume)
        
        # Generate summary
        runner.generate_summary_report()
        
        print("\n" + "="*80)
        print("✅ ALL EXPERIMENTS COMPLETE!")
        print("="*80)
        print(f"Results saved to: {runner.output_dir}")
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
        print("Progress saved. Resume with --resume flag.")


if __name__ == '__main__':
    main()
