"""
Experiment templates and utilities for dolphin acoustics research.

This module provides reusable experiment templates and analysis pipelines
for common tasks in dolphin acoustic analysis.
"""

import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
import warnings

from .io import read_ears_file
from .signal import wavelet_denoise, detect_whistles, threshold
from .batch import BatchProcessor, ResultCollector, find_data_files, select_random_files

__all__ = [
    "BasicMetricsPipeline",
    "WhistleDetectionPipeline",
    "DenoisingComparisonPipeline",
    "SpectralAnalysisPipeline",
    "run_experiment",
    "compare_methods",
]


class BasicMetricsPipeline:
    """
    Extract basic acoustic metrics from audio files.

    Metrics extracted:
    - Duration
    - RMS amplitude
    - Peak amplitude
    - Dynamic range
    - Zero-crossing rate

    Examples
    --------
    >>> pipeline = BasicMetricsPipeline()
    >>> result = pipeline(filepath)
    >>> print(f"RMS: {result['rms']:.3f}")
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def __call__(self, filepath: Path) -> Dict[str, Any]:
        """Process a file and return metrics."""
        data = read_ears_file(filepath)
        signal = data["data"]

        # Calculate metrics
        rms = float(np.sqrt(np.mean(signal**2)))
        peak = float(np.max(np.abs(signal)))

        # Dynamic range
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            signal_db = 20 * np.log10(np.abs(signal) + 1e-10)
        dynamic_range = float(np.max(signal_db) - np.min(signal_db))

        # Zero crossing rate
        zero_crossings = np.sum(np.diff(np.sign(signal)) != 0)
        zcr = float(zero_crossings / len(signal))

        return {
            "duration": data["duration"],
            "n_samples": data["n_samples"],
            "rms": rms,
            "peak": peak,
            "dynamic_range": dynamic_range,
            "zero_crossing_rate": zcr,
        }


class WhistleDetectionPipeline:
    """
    Detect and characterize dolphin whistles in audio files.

    Parameters
    ----------
    denoise : bool
        Apply wavelet denoising before detection
    power_threshold_percentile : float
        Percentile threshold for detecting ridges in spectrogram (default: 85)
        Higher values = more conservative detection
    min_duration : float
        Minimum whistle duration in seconds (default: 0.1)

    Examples
    --------
    >>> pipeline = WhistleDetectionPipeline(denoise=True)
    >>> result = pipeline(filepath)
    >>> print(f"Whistles detected: {result['n_whistles']}")
    """

    def __init__(
        self,
        denoise: bool = True,
        power_threshold_percentile: float = 85.0,
        min_duration: float = 0.1,
    ):
        self.denoise = denoise
        self.power_threshold_percentile = power_threshold_percentile
        self.min_duration = min_duration

    def __call__(self, filepath: Path) -> Dict[str, Any]:
        """Process a file and detect whistles."""
        data = read_ears_file(filepath)
        signal = data["data"]
        fs = data["fs"]

        # Optionally denoise
        if self.denoise:
            signal_clean = wavelet_denoise(signal, wavelet="db8")
        else:
            signal_clean = signal

        # Detect whistles
        whistles = detect_whistles(
            signal_clean,
            fs,
            power_threshold_percentile=self.power_threshold_percentile,
            min_duration=self.min_duration,
        )

        # Calculate statistics
        n_whistles = len(whistles)
        if n_whistles > 0:
            durations = [w["duration"] for w in whistles]
            mean_duration = float(np.mean(durations))
            total_duration = float(np.sum(durations))
            coverage = total_duration / data["duration"] * 100
        else:
            mean_duration = 0.0
            total_duration = 0.0
            coverage = 0.0

        return {
            "n_whistles": n_whistles,
            "mean_whistle_duration": mean_duration,
            "total_whistle_duration": total_duration,
            "whistle_coverage_percent": coverage,
            "recording_duration": data["duration"],
        }


class DenoisingComparisonPipeline:
    """
    Compare different denoising methods and parameters.

    Parameters
    ----------
    wavelets : List[str]
        Wavelets to compare
    levels : List[int]
        Decomposition levels to compare

    Examples
    --------
    >>> pipeline = DenoisingComparisonPipeline(
    ...     wavelets=['db4', 'db8', 'sym8'],
    ...     levels=[3, 5, 7]
    ... )
    >>> result = pipeline(filepath)
    """

    def __init__(
        self,
        wavelets: List[str] = ["db4", "db8", "sym8"],
        levels: List[int] = [3, 5, 7],
    ):
        self.wavelets = wavelets
        self.levels = levels

    def __call__(self, filepath: Path) -> Dict[str, Any]:
        """Compare denoising methods."""
        data = read_ears_file(filepath)
        signal = data["data"]

        results = {
            "original_rms": float(np.sqrt(np.mean(signal**2))),
            "original_peak": float(np.max(np.abs(signal))),
        }

        # Test each combination
        for wavelet in self.wavelets:
            for level in self.levels:
                try:
                    denoised = wavelet_denoise(signal, wavelet=wavelet, level=level)

                    # Calculate reduction metrics
                    noise = signal - denoised
                    snr = 10 * np.log10(
                        np.mean(denoised**2) / (np.mean(noise**2) + 1e-10)
                    )

                    key = f"{wavelet}_L{level}"
                    results[f"{key}_snr"] = float(snr)
                    results[f"{key}_rms"] = float(np.sqrt(np.mean(denoised**2)))

                except Exception as e:
                    # Skip this combination if it fails
                    pass

        return results


class SpectralAnalysisPipeline:
    """
    Perform spectral analysis on audio files.

    Parameters
    ----------
    freq_bands : Dict[str, tuple]
        Frequency bands to analyze (name: (low, high) in Hz)

    Examples
    --------
    >>> bands = {
    ...     'low': (0, 10000),
    ...     'whistle': (5000, 25000),
    ...     'high': (25000, 100000)
    ... }
    >>> pipeline = SpectralAnalysisPipeline(freq_bands=bands)
    >>> result = pipeline(filepath)
    """

    def __init__(self, freq_bands: Optional[Dict[str, tuple]] = None):
        if freq_bands is None:
            # Default dolphin whistle bands
            self.freq_bands = {
                "low": (0, 5000),
                "whistle_low": (5000, 15000),
                "whistle_high": (15000, 25000),
                "ultrasonic": (25000, 100000),
            }
        else:
            self.freq_bands = freq_bands

    def __call__(self, filepath: Path) -> Dict[str, Any]:
        """Perform spectral analysis."""
        from scipy import signal as scipy_signal

        data = read_ears_file(filepath)
        audio = data["data"]
        fs = data["fs"]

        # Compute power spectral density
        freqs, psd = scipy_signal.welch(
            audio, fs=fs, nperseg=min(8192, len(audio)), scaling="density"
        )

        results = {}

        # Analyze each frequency band
        for band_name, (f_low, f_high) in self.freq_bands.items():
            # Find frequencies in this band
            mask = (freqs >= f_low) & (freqs <= f_high)

            if np.any(mask):
                band_psd = psd[mask]
                band_freqs = freqs[mask]

                # Calculate band metrics
                total_power = float(np.sum(band_psd))
                mean_power = float(np.mean(band_psd))
                peak_power = float(np.max(band_psd))
                peak_freq = float(band_freqs[np.argmax(band_psd)])

                results[f"{band_name}_total_power"] = total_power
                results[f"{band_name}_mean_power"] = mean_power
                results[f"{band_name}_peak_power"] = peak_power
                results[f"{band_name}_peak_freq"] = peak_freq

        # Overall spectral centroid
        spectral_centroid = float(np.sum(freqs * psd) / np.sum(psd))
        results["spectral_centroid"] = spectral_centroid

        return results


def run_experiment(
    name: str,
    pipeline: Callable,
    data_dir: str = "data",
    pattern: str = "**/*.210",
    n_files: Optional[int] = 10,
    seed: int = 42,
    verbose: bool = True,
) -> ResultCollector:
    """
    Run a complete experiment with a pipeline.

    Parameters
    ----------
    name : str
        Experiment name
    pipeline : Callable
        Processing pipeline (callable that takes a filepath)
    data_dir : str
        Directory containing data files
    pattern : str
        Glob pattern for file selection
    n_files : int, optional
        Number of files to process (None = all files)
    seed : int
        Random seed for file selection
    verbose : bool
        Print progress information

    Returns
    -------
    ResultCollector
        Results from the experiment

    Examples
    --------
    >>> pipeline = BasicMetricsPipeline()
    >>> results = run_experiment(
    ...     name="Basic Metrics",
    ...     pipeline=pipeline,
    ...     n_files=20
    ... )
    >>> results.print_summary()
    """
    print(f"\n{'='*70}")
    print(f"EXPERIMENT: {name}")
    print(f"{'='*70}\n")

    # Find files
    all_files = find_data_files(data_dir, pattern)
    print(f"Found {len(all_files)} files")

    # Select subset
    if n_files is not None and n_files < len(all_files):
        files = select_random_files(all_files, n=n_files, seed=seed)
        print(f"Selected {len(files)} files (seed={seed})")
    else:
        files = all_files
        print(f"Processing all {len(files)} files")

    # Process
    processor = BatchProcessor(verbose=verbose)
    collector = processor.process_files(files, pipeline)

    # Summary
    print()
    collector.print_summary()

    return collector


def compare_methods(
    method_name: str,
    pipelines: Dict[str, Callable],
    data_dir: str = "data",
    pattern: str = "**/*.210",
    n_files: int = 10,
    seed: int = 42,
) -> Dict[str, ResultCollector]:
    """
    Compare multiple methods/pipelines on the same data.

    Parameters
    ----------
    method_name : str
        Name of the comparison experiment
    pipelines : Dict[str, Callable]
        Dictionary of pipeline_name: pipeline_callable
    data_dir : str
        Directory containing data files
    pattern : str
        Glob pattern for file selection
    n_files : int
        Number of files to process
    seed : int
        Random seed (ensures same files for all methods)

    Returns
    -------
    Dict[str, ResultCollector]
        Results for each pipeline

    Examples
    --------
    >>> pipelines = {
    ...     'No Denoising': WhistleDetectionPipeline(denoise=False),
    ...     'With Denoising': WhistleDetectionPipeline(denoise=True),
    ... }
    >>> results = compare_methods("Denoising Effect", pipelines)
    """
    print(f"\n{'='*70}")
    print(f"METHOD COMPARISON: {method_name}")
    print(f"{'='*70}\n")

    # Find and select files (same for all methods)
    all_files = find_data_files(data_dir, pattern)
    files = select_random_files(all_files, n=n_files, seed=seed)
    print(f"Using {len(files)} files for comparison\n")

    # Run each pipeline
    results = {}
    for pipeline_name, pipeline in pipelines.items():
        print(f"\n{'-'*70}")
        print(f"Method: {pipeline_name}")
        print(f"{'-'*70}")

        processor = BatchProcessor(verbose=False)
        collector = processor.process_files(files, pipeline)
        results[pipeline_name] = collector

        print(f"✓ Processed {len(collector.results)}/{len(files)} files")

    # Comparison summary
    print(f"\n{'='*70}")
    print(f"COMPARISON SUMMARY")
    print(f"{'='*70}\n")

    for pipeline_name, collector in results.items():
        print(f"{pipeline_name}:")
        summary = collector.summarize()
        print(f"  Success rate: {summary['success_rate']:.1f}%")
        if "metrics" in summary:
            for metric, stats in list(summary["metrics"].items())[:3]:
                print(f"  {metric}: {stats['mean']:.3f} ± {stats['std']:.3f}")
        print()

    return results
