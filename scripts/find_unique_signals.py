#!/usr/bin/env python3
"""
Find truly unique and exceptional dolphin acoustic signals.

This script looks for files with extraordinary characteristics:
1. Ultra-fast frequency sweeps (rapid chirps)
2. Extreme frequency ranges (very high or very low)
3. Multiple simultaneous vocalizations (overlapping signals)
4. Unusual click patterns (burst clicking, syncopated rhythms)
5. Harmonic structures (overtones, harmonics)
6. Rare frequency combinations
7. Long-duration sustained signals
8. High signal diversity in single recording

Usage:
    python find_unique_signals.py --file-list outputs/ears_files_list.txt --n-files 1000
"""

import sys
import argparse
from pathlib import Path
import time
import numpy as np
from scipy import signal as sp_signal
from scipy.stats import entropy
import json

sys.path.insert(0, str(Path(__file__).parent.parent))
import dolphain


def analyze_spectral_uniqueness(data, fs):
    """
    Analyze spectral characteristics for uniqueness.
    
    Returns metrics about frequency distribution, diversity, and rare features.
    """
    # Compute high-resolution spectrogram
    nperseg = 8192
    noverlap = int(0.75 * nperseg)
    
    f, t, Sxx = sp_signal.spectrogram(
        data, fs=fs, nperseg=nperseg, noverlap=noverlap,
        window='hann', scaling='density'
    )
    
    Sxx_dB = 10 * np.log10(Sxx + 1e-12)
    
    metrics = {}
    
    # 1. Frequency range diversity - how many frequency bands are active?
    freq_bands = {
        'ultra_low': (0, 2000),          # Rumbles, ambient
        'low': (2000, 10000),            # Low whistles
        'mid': (10000, 40000),           # Mid whistles, some clicks
        'high': (40000, 80000),          # High whistles, clicks
        'ultra_high': (80000, 125000),   # Ultrasonic clicks
    }
    
    active_bands = 0
    band_energies = {}
    
    for band_name, (f_low, f_high) in freq_bands.items():
        mask = (f >= f_low) & (f < f_high)
        if np.any(mask):
            band_energy = np.mean(Sxx_dB[mask, :])
            noise_floor = np.percentile(Sxx_dB[mask, :], 20)
            if band_energy > noise_floor + 10:  # 10 dB above noise
                active_bands += 1
                band_energies[band_name] = band_energy - noise_floor
    
    metrics['active_frequency_bands'] = active_bands
    metrics['band_energies'] = band_energies
    
    # 2. Spectral entropy - measure of frequency diversity
    # Higher entropy = more diverse frequency content
    freq_power = np.sum(Sxx, axis=1)
    freq_power_norm = freq_power / np.sum(freq_power)
    spectral_entropy = entropy(freq_power_norm)
    metrics['spectral_entropy'] = float(spectral_entropy)
    
    # 3. Peak frequency range - span between strongest frequencies
    threshold = np.percentile(Sxx_dB, 95)
    strong_freqs = f[np.any(Sxx_dB > threshold, axis=1)]
    if len(strong_freqs) > 0:
        metrics['peak_freq_range'] = float(strong_freqs.max() - strong_freqs.min())
        metrics['max_frequency'] = float(strong_freqs.max())
        metrics['min_frequency'] = float(strong_freqs.min())
    else:
        metrics['peak_freq_range'] = 0.0
        metrics['max_frequency'] = 0.0
        metrics['min_frequency'] = 0.0
    
    # 4. Detect simultaneous vocalizations (multiple peaks at same time)
    max_simultaneous = 0
    simultaneous_events = 0
    
    for time_idx in range(len(t)):
        col = Sxx_dB[:, time_idx]
        threshold_col = np.percentile(col, 95)
        peaks, _ = sp_signal.find_peaks(col, height=threshold_col, distance=50)
        if len(peaks) > 1:
            simultaneous_events += 1
            max_simultaneous = max(max_simultaneous, len(peaks))
    
    metrics['max_simultaneous_signals'] = max_simultaneous
    metrics['simultaneous_events'] = simultaneous_events
    
    # 5. Harmonic detection - look for overtones
    harmonics_detected = 0
    for time_idx in range(0, len(t), 5):  # Sample every 5th time point
        col = Sxx_dB[:, time_idx]
        peaks, properties = sp_signal.find_peaks(
            col, height=np.percentile(col, 90), distance=20, prominence=5
        )
        
        if len(peaks) >= 2:
            peak_freqs = f[peaks]
            # Check for harmonic relationships (2x, 3x, etc)
            for i in range(len(peak_freqs)):
                for j in range(i + 1, len(peak_freqs)):
                    ratio = peak_freqs[j] / peak_freqs[i]
                    if 1.8 < ratio < 2.2 or 2.8 < ratio < 3.2:  # 2x or 3x harmonic
                        harmonics_detected += 1
                        break
    
    metrics['harmonic_events'] = harmonics_detected
    
    return metrics, Sxx_dB, f, t


def detect_ultra_fast_sweeps(Sxx_dB, f, t, fs):
    """
    Detect exceptionally fast frequency sweeps (>10 kHz/sec).
    """
    fast_sweeps = []
    
    nperseg = 8192
    threshold = np.percentile(Sxx_dB, 95)
    
    chirps = []
    for time_idx in range(len(t)):
        col = Sxx_dB[:, time_idx]
        peaks, _ = sp_signal.find_peaks(col, height=threshold, distance=50)
        
        # Try to extend existing chirps
        extended = set()
        for chirp in chirps:
            if chirp['end_idx'] == time_idx - 1:
                last_freq = chirp['freq_indices'][-1]
                if len(peaks) > 0:
                    closest = peaks[np.argmin(np.abs(peaks - last_freq))]
                    if abs(closest - last_freq) < 15:
                        chirp['freq_indices'].append(closest)
                        chirp['end_idx'] = time_idx
                        extended.add(closest)
        
        # Start new chirps
        for peak in peaks:
            if peak not in extended:
                chirps.append({
                    'freq_indices': [peak],
                    'end_idx': time_idx,
                    'start_idx': time_idx
                })
    
    # Find fast sweeps
    for chirp in chirps:
        if len(chirp['freq_indices']) < 3:
            continue
        
        freq_indices = np.array(chirp['freq_indices'])
        freqs = f[freq_indices]
        
        time_indices = list(range(chirp['start_idx'], chirp['end_idx'] + 1))
        times = t[time_indices[:len(freqs)]]
        
        if len(times) < 2:
            continue
        
        duration = times[-1] - times[0]
        freq_change = abs(freqs[-1] - freqs[0])
        
        if duration > 0:
            sweep_rate = freq_change / duration
            
            # Ultra-fast sweep: >10 kHz/sec
            if sweep_rate > 10000:
                fast_sweeps.append({
                    'sweep_rate': float(sweep_rate),
                    'freq_change': float(freq_change),
                    'duration': float(duration),
                    'start_freq': float(freqs[0]),
                    'end_freq': float(freqs[-1])
                })
    
    return fast_sweeps


def detect_unusual_click_patterns(data, fs):
    """
    Detect unusual click patterns: burst clicking, syncopated rhythms, etc.
    """
    # High-pass filter for clicks
    nyquist = fs / 2.0
    sos = sp_signal.butter(6, [20000/nyquist, 0.999], btype='bandpass', output='sos')
    filtered = sp_signal.sosfiltfilt(sos, data)
    
    # Envelope
    analytic = sp_signal.hilbert(filtered)
    envelope = np.abs(analytic)
    
    # Smooth minimally
    kernel_size = int(fs * 0.0005)
    if kernel_size % 2 == 0:
        kernel_size += 1
    if kernel_size >= 3:
        envelope = sp_signal.medfilt(envelope, kernel_size=kernel_size)
    
    threshold = np.percentile(envelope, 99)
    peaks, _ = sp_signal.find_peaks(envelope, height=threshold, distance=int(fs*0.001))
    
    if len(peaks) < 5:
        return {}
    
    peak_times = peaks / fs
    icis = np.diff(peak_times)
    
    patterns = {}
    
    # 1. Burst clicking (very rapid, <5ms ICI)
    burst_clicks = np.sum(icis < 0.005)
    patterns['burst_clicks'] = int(burst_clicks)
    
    # 2. Rhythmic regularity (low CV)
    if len(icis) > 2:
        cv = np.std(icis) / np.mean(icis) if np.mean(icis) > 0 else 999
        patterns['click_regularity_cv'] = float(cv)
        patterns['is_highly_regular'] = cv < 0.3
    
    # 3. Bimodal ICI distribution (two different click rates)
    if len(icis) > 10:
        hist, bins = np.histogram(icis, bins=20)
        peaks_in_hist, _ = sp_signal.find_peaks(hist, prominence=2)
        patterns['ici_modes'] = len(peaks_in_hist)
        patterns['is_bimodal'] = len(peaks_in_hist) >= 2
    
    # 4. Acceleration/deceleration patterns
    if len(icis) > 5:
        ici_changes = np.diff(icis)
        increasing_trend = np.sum(ici_changes > 0) / len(ici_changes)
        decreasing_trend = np.sum(ici_changes < 0) / len(ici_changes)
        
        patterns['click_acceleration'] = increasing_trend > 0.7  # Slowing down
        patterns['click_deceleration'] = decreasing_trend > 0.7  # Speeding up
    
    patterns['total_clicks'] = len(peaks)
    patterns['mean_ici'] = float(np.mean(icis))
    patterns['ici_range'] = float(np.max(icis) - np.min(icis))
    
    return patterns


def calculate_uniqueness_score(spectral_metrics, fast_sweeps, click_patterns):
    """
    Calculate a uniqueness score (0-100) based on rare and exceptional features.
    
    Higher scores indicate more unique/interesting signals.
    """
    score = 0.0
    
    # === SPECTRAL UNIQUENESS (40 points) ===
    
    # Multiple active frequency bands (0-15 points)
    active_bands = spectral_metrics.get('active_frequency_bands', 0)
    score += min(15, active_bands * 3)  # 3 pts per band, max 15
    
    # Spectral diversity (0-10 points)
    spectral_entropy = spectral_metrics.get('spectral_entropy', 0)
    score += min(10, (spectral_entropy / 5.0) * 10)  # Normalize by typical max ~5
    
    # Extreme frequency range (0-10 points)
    freq_range = spectral_metrics.get('peak_freq_range', 0)
    score += min(10, (freq_range / 50000) * 10)  # 50 kHz+ is exceptional
    
    # Rare extreme frequencies (0-5 points)
    max_freq = spectral_metrics.get('max_frequency', 0)
    if max_freq > 100000:  # Ultra-high
        score += 5
    elif max_freq > 80000:
        score += 3
    
    # === SPECIAL FEATURES (30 points) ===
    
    # Simultaneous vocalizations (0-10 points)
    max_simultaneous = spectral_metrics.get('max_simultaneous_signals', 0)
    if max_simultaneous >= 4:
        score += 10
    elif max_simultaneous >= 3:
        score += 7
    elif max_simultaneous >= 2:
        score += 4
    
    # Harmonics (0-10 points)
    harmonics = spectral_metrics.get('harmonic_events', 0)
    score += min(10, harmonics * 0.5)  # 0.5 pts per harmonic event
    
    # Ultra-fast sweeps (0-10 points)
    if len(fast_sweeps) > 0:
        fastest = max([s['sweep_rate'] for s in fast_sweeps])
        if fastest > 50000:  # >50 kHz/sec
            score += 10
        elif fastest > 30000:
            score += 7
        elif fastest > 15000:
            score += 5
        elif fastest > 10000:
            score += 3
    
    # === CLICK PATTERN UNIQUENESS (30 points) ===
    
    # Burst clicking (0-8 points)
    burst_clicks = click_patterns.get('burst_clicks', 0)
    score += min(8, burst_clicks * 0.2)
    
    # Unusual patterns (0-12 points)
    if click_patterns.get('is_bimodal', False):
        score += 6  # Two different click rates
    if click_patterns.get('click_acceleration', False) or click_patterns.get('click_deceleration', False):
        score += 6  # Changing tempo
    
    # High regularity or high irregularity (0-5 points)
    cv = click_patterns.get('click_regularity_cv', 999)
    if click_patterns.get('is_highly_regular', False):
        score += 5  # Exceptionally regular
    elif cv > 0.8:
        score += 3  # Exceptionally irregular
    
    # Click diversity (0-5 points)
    ici_range = click_patterns.get('ici_range', 0)
    score += min(5, (ici_range / 0.05) * 5)  # Wide range of ICIs
    
    return min(100, score)


def analyze_file(file_path):
    """Analyze a single file for uniqueness."""
    try:
        # Read file
        data_dict = dolphain.read_ears_file(file_path)
        data = data_dict['data']
        fs = data_dict['sample_rate']
        
        # Denoise
        data_clean = dolphain.wavelet_denoise(data, wavelet='db8', level=5)
        
        # Analyze spectral characteristics
        spectral_metrics, Sxx_dB, f, t = analyze_spectral_uniqueness(data_clean, fs)
        
        # Detect ultra-fast sweeps
        fast_sweeps = detect_ultra_fast_sweeps(Sxx_dB, f, t, fs)
        
        # Analyze click patterns
        click_patterns = detect_unusual_click_patterns(data_clean, fs)
        
        # Calculate uniqueness score
        uniqueness_score = calculate_uniqueness_score(
            spectral_metrics, fast_sweeps, click_patterns
        )
        
        result = {
            'filename': str(file_path),
            'uniqueness_score': float(uniqueness_score),
            'spectral_metrics': spectral_metrics,
            'n_fast_sweeps': len(fast_sweeps),
            'fast_sweeps': fast_sweeps[:5],  # Keep top 5
            'click_patterns': click_patterns,
        }
        
        return result
        
    except Exception as e:
        return {
            'filename': str(file_path),
            'error': str(e),
            'uniqueness_score': 0.0
        }


def run_unique_signal_search(file_list_path, n_files, output_dir):
    """Run the unique signal search."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print("=" * 80)
    print("🌟 UNIQUE SIGNAL DETECTION")
    print("=" * 80)
    print(f"Sample size: {n_files} files")
    print(f"Output: {output_dir}")
    print()
    print("Looking for exceptional features:")
    print("  🎵 Ultra-fast frequency sweeps (>10 kHz/sec)")
    print("  🎚️  Extreme frequency ranges (very high/low)")
    print("  🎼 Multiple simultaneous vocalizations")
    print("  🥁 Unusual click patterns (bursts, rhythms)")
    print("  🎹 Harmonic structures")
    print("  🌈 High spectral diversity")
    print()
    
    # Load file list
    with open(file_list_path, 'r') as f:
        all_files = [Path(line.strip()) for line in f if line.strip()]
    
    print(f"📋 Loaded {len(all_files)} files from list")
    
    # Sample
    import random
    if len(all_files) > n_files:
        file_list = random.sample(all_files, n_files)
        print(f"   Sampling {n_files} files randomly")
    else:
        file_list = all_files
        print(f"   Using all {len(file_list)} files")
    
    print()
    
    # Process files
    results = []
    start_time = time.time()
    
    checkpoint_file = output_dir / 'checkpoint.json'
    
    for i, file_path in enumerate(file_list, 1):
        file_start = time.time()
        
        print(f"[{i}/{len(file_list)}] {file_path.name}...", end=' ', flush=True)
        
        result = analyze_file(file_path)
        results.append(result)
        
        file_time = time.time() - file_start
        score = result.get('uniqueness_score', 0)
        
        print(f"✓ Score: {score:.1f} ({file_time:.1f}s)")
        
        # Checkpoint every 10 files
        if i % 10 == 0:
            with open(checkpoint_file, 'w') as f:
                json.dump({'results': results, 'n_processed': i}, f, indent=2)
    
    # Sort by uniqueness score
    results.sort(key=lambda x: x.get('uniqueness_score', 0), reverse=True)
    
    # Save final results
    results_file = output_dir / 'results.json'
    with open(results_file, 'w') as f:
        json.dump({
            'results': results,
            'n_analyzed': len(results),
            'detection_type': 'unique_signals'
        }, f, indent=2)
    
    # Save summary
    summary = {
        'total_files': len(results),
        'avg_uniqueness_score': np.mean([r.get('uniqueness_score', 0) for r in results]),
        'max_uniqueness_score': max([r.get('uniqueness_score', 0) for r in results]),
        'files_with_fast_sweeps': sum(1 for r in results if r.get('n_fast_sweeps', 0) > 0),
        'files_with_harmonics': sum(1 for r in results if r.get('spectral_metrics', {}).get('harmonic_events', 0) > 0),
        'files_with_simultaneous': sum(1 for r in results if r.get('spectral_metrics', {}).get('max_simultaneous_signals', 0) >= 2),
        'top_20_files': [r['filename'] for r in results[:20]]
    }
    
    summary_file = output_dir / 'summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    elapsed = time.time() - start_time
    print()
    print("=" * 80)
    print("✅ UNIQUE SIGNAL SEARCH COMPLETE!")
    print("=" * 80)
    print(f"⏱️  Total time: {elapsed/60:.1f} minutes")
    print(f"📊 Files analyzed: {len(results)}")
    print(f"⭐ Avg uniqueness: {summary['avg_uniqueness_score']:.1f}")
    print(f"🌟 Max uniqueness: {summary['max_uniqueness_score']:.1f}")
    print(f"🚀 Files with fast sweeps: {summary['files_with_fast_sweeps']}")
    print(f"🎹 Files with harmonics: {summary['files_with_harmonics']}")
    print(f"🎼 Files with simultaneous signals: {summary['files_with_simultaneous']}")
    print()
    print("🏆 Top 10 most unique files:")
    for i, r in enumerate(results[:10], 1):
        filename = Path(r['filename']).name
        score = r.get('uniqueness_score', 0)
        n_sweeps = r.get('n_fast_sweeps', 0)
        harmonics = r.get('spectral_metrics', {}).get('harmonic_events', 0)
        print(f"  {i:2d}. {filename} - Score: {score:.1f} (Sweeps: {n_sweeps}, Harmonics: {harmonics})")
    
    print()
    print(f"📁 Results saved to: {output_dir}/")
    print(f"   - results.json (full results)")
    print(f"   - summary.json (statistics)")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Find unique and exceptional dolphin acoustic signals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python find_unique_signals.py --file-list outputs/ears_files_list.txt --n-files 1000
  
  python find_unique_signals.py --file-list outputs/ears_files_list.txt --n-files 500 \\
      --output-dir experiments/unique_signals_test

This search looks for:
  - Ultra-fast frequency sweeps (>10 kHz/sec)
  - Extreme frequency ranges (very high or very low)
  - Multiple simultaneous vocalizations
  - Unusual click patterns (bursts, syncopated rhythms)
  - Harmonic structures
  - High spectral diversity
  - Other rare and exceptional acoustic features
        """
    )
    
    parser.add_argument(
        '--file-list',
        type=Path,
        required=True,
        help='Pre-generated file list (one file per line)'
    )
    parser.add_argument(
        '--n-files',
        type=int,
        default=1000,
        help='Number of files to analyze (default: 1000)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default='experiments/unique_signals',
        help='Output directory (default: experiments/unique_signals)'
    )
    
    args = parser.parse_args()
    
    # Validate
    if not args.file_list.exists():
        print(f"❌ Error: File list not found: {args.file_list}")
        sys.exit(1)
    
    # Run
    run_unique_signal_search(
        file_list_path=args.file_list,
        n_files=args.n_files,
        output_dir=args.output_dir
    )


if __name__ == '__main__':
    main()
