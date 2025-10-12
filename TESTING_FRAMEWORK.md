# Testing and Experiment Framework

This document describes the testing and experimentation framework for the dolphain library.

## Overview

The framework provides three layers:

1. **Unit Tests** - Verify individual components work correctly
2. **Batch Processing** - Process multiple files efficiently
3. **Experiment Templates** - Reusable analysis pipelines

## Unit Tests

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_batch.py -v

# Run specific test class
pytest tests/test_batch.py::TestBatchProcessor -v

# Run with coverage
pytest tests/ --cov=dolphain --cov-report=html
```

### Test Structure

```
tests/
├── test_ears_reader.py   # Core I/O and signal processing tests
└── test_batch.py         # Batch processing and pipeline tests
```

### Writing New Tests

```python
import pytest
import dolphain

class TestMyFeature:
    """Test my new feature."""

    @pytest.fixture
    def sample_data(self):
        """Provide sample data for tests."""
        return dolphain.read_ears_file("data/sample.210")

    def test_feature_works(self, sample_data):
        """Test that the feature works."""
        result = dolphain.my_feature(sample_data)
        assert result is not None
```

## Batch Processing

### Basic Usage

Process multiple files through a pipeline:

```python
import dolphain

# Define a processing pipeline
def my_pipeline(filepath):
    data = dolphain.read_ears_file(filepath)
    # ... process data ...
    return {
        "metric1": value1,
        "metric2": value2,
    }

# Find and select files
files = dolphain.find_data_files("data", "**/*.210")
subset = dolphain.select_random_files(files, n=10, seed=42)

# Process with progress tracking
processor = dolphain.BatchProcessor(verbose=True)
collector = processor.process_files(subset, my_pipeline)

# View results
collector.print_summary()
```

### Features

- **Automatic timing**: Track processing time per file and total
- **Error handling**: Continue processing even if some files fail
- **Result collection**: Aggregate results and compute statistics
- **Progress feedback**: Optional verbose output

### Result Analysis

```python
# Get summary statistics
summary = collector.summarize()

print(f"Success rate: {summary['success_rate']:.1f}%")
print(f"Mean processing time: {summary['timings']['per_file']['mean']:.3f}s")

# Access raw results
for result in collector.results:
    print(f"{result['file']}: {result['metric1']:.3f}")

# Check for errors
if collector.errors:
    print(f"Errors occurred in {len(collector.errors)} files")
```

## Experiment Templates

Pre-built pipelines for common analysis tasks.

### 1. Basic Metrics Pipeline

Extract fundamental acoustic metrics:

```python
pipeline = dolphain.BasicMetricsPipeline()

# Run on a single file
result = pipeline(filepath)
print(f"RMS: {result['rms']:.3f}")
print(f"Peak: {result['peak']:.3f}")

# Or use in batch processing
collector = dolphain.run_experiment(
    name="Basic Metrics Analysis",
    pipeline=pipeline,
    n_files=20
)
```

**Metrics extracted:**

- Duration
- RMS amplitude
- Peak amplitude
- Dynamic range
- Zero-crossing rate

### 2. Whistle Detection Pipeline

Detect and characterize dolphin whistles:

```python
# With denoising
pipeline = dolphain.WhistleDetectionPipeline(
    denoise=True,
    threshold_factor=3.0
)

result = pipeline(filepath)
print(f"Whistles detected: {result['n_whistles']}")
print(f"Coverage: {result['whistle_coverage_percent']:.1f}%")
```

**Metrics extracted:**

- Number of whistles
- Mean whistle duration
- Total whistle duration
- Whistle coverage percentage

### 3. Denoising Comparison Pipeline

Compare wavelet denoising methods:

```python
pipeline = dolphain.DenoisingComparisonPipeline(
    wavelets=['db4', 'db8', 'sym8'],
    levels=[3, 5, 7]
)

result = pipeline(filepath)
# Results include SNR and RMS for each wavelet/level combination
print(f"db8_L5_snr: {result['db8_L5_snr']:.2f} dB")
```

### 4. Spectral Analysis Pipeline

Analyze frequency content:

```python
# Define custom frequency bands
bands = {
    'low': (0, 5000),
    'whistle_low': (5000, 15000),
    'whistle_high': (15000, 25000),
    'ultrasonic': (25000, 100000),
}

pipeline = dolphain.SpectralAnalysisPipeline(freq_bands=bands)

result = pipeline(filepath)
print(f"Whistle band power: {result['whistle_low_total_power']:.3e}")
print(f"Peak frequency: {result['whistle_low_peak_freq']:.0f} Hz")
```

## Complete Experiment Workflow

### Simple Experiment

```python
import dolphain

# Create pipeline
pipeline = dolphain.BasicMetricsPipeline()

# Run experiment
results = dolphain.run_experiment(
    name="File Quality Assessment",
    pipeline=pipeline,
    data_dir="data",
    pattern="**/*.210",
    n_files=50,
    seed=42,
    verbose=True
)

# Results are automatically printed
# Access programmatically
summary = results.summarize()
```

### Method Comparison

Compare different approaches on the same data:

```python
import dolphain

# Define methods to compare
methods = {
    'No Denoising': dolphain.WhistleDetectionPipeline(denoise=False),
    'DB4 Wavelet': dolphain.WhistleDetectionPipeline(denoise=True),
    'Aggressive Threshold': dolphain.WhistleDetectionPipeline(
        denoise=True,
        threshold_factor=5.0
    ),
}

# Compare (same files for all methods)
results = dolphain.compare_methods(
    method_name="Whistle Detection Methods",
    pipelines=methods,
    n_files=30,
    seed=42
)

# Analyze differences
for method_name, collector in results.items():
    summary = collector.summarize()
    print(f"\n{method_name}:")
    print(f"  Mean whistles detected: {summary['metrics']['n_whistles']['mean']:.1f}")
```

## Custom Pipelines

### Creating a Custom Pipeline

```python
from pathlib import Path
from typing import Dict, Any
import dolphain
import numpy as np

class MyCustomPipeline:
    """My custom analysis pipeline."""

    def __init__(self, param1: float = 1.0, param2: bool = True):
        """Initialize with parameters."""
        self.param1 = param1
        self.param2 = param2

    def __call__(self, filepath: Path) -> Dict[str, Any]:
        """
        Process a file.

        Parameters
        ----------
        filepath : Path
            Path to EARS file

        Returns
        -------
        Dict[str, Any]
            Dictionary of results (all values should be numeric or strings)
        """
        # Read data
        data = dolphain.read_ears_file(filepath)
        signal = data["data"]

        # Your analysis here
        result = self.my_analysis(signal)

        # Return results as dict
        return {
            "my_metric": result,
            "duration": data["duration"],
            # ... more metrics ...
        }

    def my_analysis(self, signal):
        """Your analysis implementation."""
        return np.mean(signal ** 2)

# Use it
pipeline = MyCustomPipeline(param1=2.5)
results = dolphain.run_experiment("My Experiment", pipeline, n_files=10)
```

### Pipeline Best Practices

1. **Return numeric metrics**: Makes aggregation/statistics easy
2. **Handle errors gracefully**: Use try/except for robust processing
3. **Include metadata**: Duration, sample count, etc.
4. **Document parameters**: Clear docstrings for reproducibility
5. **Make it reusable**: Class-based with configurable parameters

## Reproducibility

### Fixed Seeds

Always use fixed random seeds for reproducibility:

```python
# This will always select the same files
files = dolphain.select_random_files(all_files, n=20, seed=42)

# Run multiple times - same results
results1 = dolphain.run_experiment("Test", pipeline, n_files=20, seed=42)
results2 = dolphain.run_experiment("Test", pipeline, n_files=20, seed=42)
# results1 and results2 used the same files
```

### Saving Results

```python
import pandas as pd
import json

# Save results to CSV
df = pd.DataFrame(collector.results)
df.to_csv("results.csv", index=False)

# Save summary as JSON
summary = collector.summarize()
with open("summary.json", "w") as f:
    json.dump(summary, f, indent=2)
```

## Example Experiments

### Experiment 1: Data Quality Assessment

```python
import dolphain

# Assess overall data quality
pipeline = dolphain.BasicMetricsPipeline()
results = dolphain.run_experiment(
    name="Data Quality Assessment",
    pipeline=pipeline,
    n_files=100,
    seed=42
)

# Check for outliers
summary = results.summarize()
rms_mean = summary['metrics']['rms']['mean']
rms_std = summary['metrics']['rms']['std']

outliers = [
    r for r in results.results
    if abs(r['rms'] - rms_mean) > 3 * rms_std
]
print(f"Found {len(outliers)} outlier files")
```

### Experiment 2: Optimal Denoising Parameters

```python
import dolphain

# Test different denoising parameters
pipeline = dolphain.DenoisingComparisonPipeline(
    wavelets=['db4', 'db6', 'db8', 'sym6', 'sym8'],
    levels=[3, 4, 5, 6, 7]
)

results = dolphain.run_experiment(
    name="Denoising Parameter Optimization",
    pipeline=pipeline,
    n_files=50,
    seed=42
)

# Find best parameters (highest mean SNR)
summary = results.summarize()
best_snr = max(
    (metric, stats['mean'])
    for metric, stats in summary['metrics'].items()
    if metric.endswith('_snr')
)
print(f"Best method: {best_snr[0]} with SNR={best_snr[1]:.2f} dB")
```

### Experiment 3: Whistle Detection Performance

```python
import dolphain

# Compare detection methods
methods = {
    'Baseline': dolphain.WhistleDetectionPipeline(
        denoise=False,
        threshold_factor=3.0
    ),
    'Denoised': dolphain.WhistleDetectionPipeline(
        denoise=True,
        threshold_factor=3.0
    ),
    'Conservative': dolphain.WhistleDetectionPipeline(
        denoise=True,
        threshold_factor=5.0
    ),
}

results = dolphain.compare_methods(
    method_name="Whistle Detection Comparison",
    pipelines=methods,
    n_files=100,
    seed=42
)

# Analyze trade-offs
for name, collector in results.items():
    summary = collector.summarize()
    metrics = summary['metrics']
    print(f"\n{name}:")
    print(f"  Whistles per file: {metrics['n_whistles']['mean']:.2f}")
    print(f"  Coverage: {metrics['whistle_coverage_percent']['mean']:.1f}%")
```

## Tips & Tricks

### Debugging Pipelines

Test on a single file first:

```python
# Test pipeline on one file
test_file = dolphain.find_data_files("data")[0]
result = pipeline(test_file)
print(result)  # Check output format

# Then run on multiple files
results = dolphain.run_experiment("Test", pipeline, n_files=5)
```

### Performance Optimization

```python
# Time your pipeline
with dolphain.timer("Pipeline execution"):
    result = pipeline(filepath)

# Process in batches for large datasets
all_files = dolphain.find_data_files("data")
for i in range(0, len(all_files), 100):
    batch = all_files[i:i+100]
    collector = processor.process_files(batch, pipeline)
    # Save intermediate results
```

### Error Analysis

```python
# Check which files failed
if collector.errors:
    print("\nFailed files:")
    for error in collector.errors:
        print(f"  {error['file']}: {error['error_type']}")

    # Try to process failed files with more debugging
    failed_files = [Path(e['file']) for e in collector.errors]
    for f in failed_files:
        try:
            result = pipeline(f)
        except Exception as e:
            print(f"\nDetailed error for {f.name}:")
            import traceback
            traceback.print_exc()
```

## Integration with Notebooks

Use in Jupyter notebooks for interactive exploration:

```python
# In notebook cell
import dolphain
import matplotlib.pyplot as plt

# Run experiment
pipeline = dolphain.WhistleDetectionPipeline()
results = dolphain.run_experiment("Whistle Analysis", pipeline, n_files=20)

# Plot results
import pandas as pd
df = pd.DataFrame(results.results)

plt.figure(figsize=(10, 6))
plt.hist(df['n_whistles'], bins=20)
plt.xlabel('Number of Whistles')
plt.ylabel('Frequency')
plt.title('Whistle Count Distribution')
plt.show()
```

## Next Steps

1. Run existing tests: `pytest tests/ -v`
2. Try example experiments in `examples/batch_experiments.ipynb`
3. Create your own custom pipeline
4. Compare different analysis methods
5. Document findings and share results

For questions or contributions, see the main README.
