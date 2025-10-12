"""
Batch processing utilities for running experiments on multiple EARS files.

This module provides tools for:
- Discovering and selecting data files
- Running pipelines on multiple files
- Collecting and summarizing results
- Performance timing and monitoring
"""

import time
import numpy as np
from pathlib import Path
from typing import List, Dict, Callable, Any, Optional
import warnings


__all__ = [
    "find_data_files",
    "select_random_files",
    "BatchProcessor",
    "timer",
    "ResultCollector",
]


def find_data_files(data_dir: str = "data", pattern: str = "**/*.210") -> List[Path]:
    """
    Find all EARS data files in a directory.

    Parameters
    ----------
    data_dir : str
        Root directory to search
    pattern : str
        Glob pattern for files (default: '**/*.210' finds all .210 files)

    Returns
    -------
    List[Path]
        List of Path objects for matching files

    Examples
    --------
    >>> files = find_data_files('data', '**/*.210')
    >>> print(f"Found {len(files)} files")
    """
    data_path = Path(data_dir)
    files = sorted(data_path.glob(pattern))
    return files


def select_random_files(
    files: List[Path], n: int = 10, seed: Optional[int] = 42
) -> List[Path]:
    """
    Select a random subset of files.

    Parameters
    ----------
    files : List[Path]
        List of file paths
    n : int
        Number of files to select
    seed : int, optional
        Random seed for reproducibility (default: 42)

    Returns
    -------
    List[Path]
        Random subset of files

    Examples
    --------
    >>> all_files = find_data_files('data')
    >>> subset = select_random_files(all_files, n=10, seed=42)
    """
    if seed is not None:
        np.random.seed(seed)

    n = min(n, len(files))
    indices = np.random.choice(len(files), size=n, replace=False)
    return [files[i] for i in sorted(indices)]


class timer:
    """
    Context manager for timing code blocks.

    Examples
    --------
    >>> with timer("Processing file"):
    ...     # Your code here
    ...     pass
    Processing file: 1.234 seconds
    """

    def __init__(self, description: str = "Operation", verbose: bool = True):
        self.description = description
        self.verbose = verbose
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
        if self.verbose:
            print(f"{self.description}: {self.elapsed:.3f} seconds")


class ResultCollector:
    """
    Collect and summarize results from batch processing.

    Examples
    --------
    >>> collector = ResultCollector()
    >>> collector.add_result('file1.210', {'snr': 15.3, 'duration': 30.0})
    >>> collector.add_result('file2.210', {'snr': 12.1, 'duration': 30.0})
    >>> summary = collector.summarize()
    """

    def __init__(self):
        self.results = []
        self.errors = []
        self.timings = {}

    def add_result(self, filepath: str, result: Dict[str, Any]):
        """Add a successful result."""
        self.results.append({"file": str(filepath), **result})

    def add_error(self, filepath: str, error: Exception):
        """Record an error."""
        self.errors.append(
            {
                "file": str(filepath),
                "error": str(error),
                "error_type": type(error).__name__,
            }
        )

    def add_timing(self, operation: str, elapsed: float):
        """Record timing for an operation."""
        if operation not in self.timings:
            self.timings[operation] = []
        self.timings[operation].append(elapsed)

    @property
    def successful(self) -> int:
        """Number of successful results (backwards-compatible helper)."""

        return len(self.results)

    @property
    def failed(self) -> int:
        """Number of failed results (backwards-compatible helper)."""

        return len(self.errors)

    def summarize(self) -> Dict[str, Any]:
        """
        Generate summary statistics.

        Returns
        -------
        Dict[str, Any]
            Summary statistics including counts, timings, and metric summaries
        """
        summary = {
            "total_files": len(self.results) + len(self.errors),
            "successful": len(self.results),
            "failed": len(self.errors),
            "success_rate": (
                len(self.results) / (len(self.results) + len(self.errors)) * 100
                if self.results or self.errors
                else 0
            ),
        }

        # Add timing statistics
        if self.timings:
            summary["timings"] = {}
            for op, times in self.timings.items():
                summary["timings"][op] = {
                    "mean": np.mean(times),
                    "std": np.std(times),
                    "min": np.min(times),
                    "max": np.max(times),
                    "total": np.sum(times),
                }

        # Add metric statistics if results have numeric values
        if self.results:
            # Find all numeric keys
            first_result = self.results[0]
            numeric_keys = [
                k
                for k, v in first_result.items()
                if k != "file" and isinstance(v, (int, float, np.number))
            ]

            summary["metrics"] = {}
            for key in numeric_keys:
                values = [r[key] for r in self.results if key in r]
                if values:
                    summary["metrics"][key] = {
                        "mean": np.mean(values),
                        "std": np.std(values),
                        "min": np.min(values),
                        "max": np.max(values),
                        "median": np.median(values),
                    }

        return summary

    def print_summary(self):
        """Print a formatted summary of results."""
        summary = self.summarize()

        print("=" * 70)
        print("BATCH PROCESSING SUMMARY")
        print("=" * 70)
        print(f"Total files processed: {summary['total_files']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success rate: {summary['success_rate']:.1f}%")

        if "timings" in summary:
            print("\n" + "-" * 70)
            print("TIMING STATISTICS")
            print("-" * 70)
            for op, stats in summary["timings"].items():
                print(f"\n{op}:")
                print(f"  Total: {stats['total']:.2f}s")
                print(f"  Mean:  {stats['mean']:.3f}s ± {stats['std']:.3f}s")
                print(f"  Range: [{stats['min']:.3f}s, {stats['max']:.3f}s]")

        if "metrics" in summary:
            print("\n" + "-" * 70)
            print("METRIC STATISTICS")
            print("-" * 70)
            for metric, stats in summary["metrics"].items():
                print(f"\n{metric}:")
                print(f"  Mean:   {stats['mean']:.3f} ± {stats['std']:.3f}")
                print(f"  Median: {stats['median']:.3f}")
                print(f"  Range:  [{stats['min']:.3f}, {stats['max']:.3f}]")

        if self.errors:
            print("\n" + "-" * 70)
            print(f"ERRORS ({len(self.errors)} files)")
            print("-" * 70)
            for err in self.errors[:5]:  # Show first 5 errors
                print(f"  {Path(err['file']).name}: {err['error_type']}")
            if len(self.errors) > 5:
                print(f"  ... and {len(self.errors) - 5} more")

        print("=" * 70)


class BatchProcessor:
    """
    Process multiple files through a pipeline of operations.

    Examples
    --------
    >>> def my_pipeline(filepath):
    ...     data = dolphain.read_ears_file(filepath)
    ...     # Process data...
    ...     return {'metric': 123.45}
    >>>
    >>> processor = BatchProcessor(verbose=True)
    >>> results = processor.process_files(file_list, my_pipeline)
    """

    def __init__(self, verbose: bool = True):
        """
        Initialize batch processor.

        Parameters
        ----------
        verbose : bool
            If True, print progress information
        """
        self.verbose = verbose
        self.collector = ResultCollector()

    def process_file(
        self, filepath: Path, pipeline: Callable
    ) -> Optional[Dict[str, Any]]:
        """
        Process a single file through the pipeline.

        Parameters
        ----------
        filepath : Path
            Path to the file to process
        pipeline : Callable
            Function that takes a filepath and returns a dict of results

        Returns
        -------
        Optional[Dict[str, Any]]
            Results dict if successful, None if error
        """
        try:
            with timer(f"  Processing {filepath.name}", verbose=False) as t:
                result = pipeline(filepath)

            self.collector.add_result(filepath, result)
            self.collector.add_timing("per_file", t.elapsed)

            if self.verbose:
                print(f"✓ {filepath.name} ({t.elapsed:.2f}s)")

            return result

        except Exception as e:
            self.collector.add_error(filepath, e)
            if self.verbose:
                print(f"✗ {filepath.name}: {type(e).__name__}: {str(e)}")
            return None

    def process_files(
        self, filepaths: List[Path], pipeline: Callable, max_files: Optional[int] = None
    ) -> ResultCollector:
        """
        Process multiple files through the pipeline.

        Parameters
        ----------
        filepaths : List[Path]
            List of file paths to process
        pipeline : Callable
            Function that takes a filepath and returns a dict of results
        max_files : int, optional
            Maximum number of files to process (useful for testing)

        Returns
        -------
        ResultCollector
            Collector with all results and statistics

        Examples
        --------
        >>> files = find_data_files('data')[:10]
        >>> processor = BatchProcessor()
        >>> collector = processor.process_files(files, my_pipeline)
        >>> collector.print_summary()
        """
        if max_files:
            filepaths = filepaths[:max_files]

        print(f"\nProcessing {len(filepaths)} files...")
        print("-" * 70)

        with timer("Total batch processing", verbose=False) as total_timer:
            for filepath in filepaths:
                self.process_file(filepath, pipeline)

        self.collector.add_timing("total_batch", total_timer.elapsed)

        print("-" * 70)
        print(f"Completed in {total_timer.elapsed:.2f}s\n")

        return self.collector
