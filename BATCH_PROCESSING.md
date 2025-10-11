# Batch Processing Framework - Quick Start

## Overview

The Dolphain batch processing framework enables efficient analysis of multiple EARS files with:

- **Automated file discovery and selection**
- **Pipeline-based processing**
- **Performance timing and monitoring**
- **Result collection and aggregation**
- **Statistical summaries**
- **Error handling**

## Quick Example

```python
import dolphain

# Define your analysis pipeline
def my_pipeline(filepath):
    data = dolphain.read_ears_file(filepath)
    acoustic = data['data']

    return {
        'duration': data['duration'],
        'rms': np.sqrt(np.mean(acoustic**2)),
        'peak': np.max(np.abs(acoustic))
    }

# Find and select files
files = dolphain.find_data_files('data', '**/*.210')
subset = dolphain.select_random_files(files, n=10, seed=42)

# Run batch processing
processor = dolphain.BatchProcessor(verbose=True)
collector = processor.process_files(subset, my_pipeline)

# View results
collector.print_summary()
```

## Key Components

### 1. File Discovery

```python
# Find all .210 files
files = dolphain.find_data_files('data', '**/*.210')

# Find specific patterns
files = dolphain.find_data_files('data', '**/Buoy*/*.190')
```

### 2. Random Selection

```python
# Select random subset with reproducible seed
subset = dolphain.select_random_files(files, n=10, seed=42)
```

### 3. Pipeline Function

Your pipeline should:

- Accept a `Path` object
- Return a `dict` with metrics
- Handle its own errors (or let BatchProcessor catch them)

```python
def pipeline(filepath):
    # Load data
    data = dolphain.read_ears_file(filepath)

    # Process
    result = your_analysis(data)

    # Return metrics dict
    return {
        'metric1': value1,
        'metric2': value2,
    }
```

### 4. Batch Processing

```python
processor = dolphain.BatchProcessor(verbose=True)
collector = processor.process_files(files, pipeline)
```

### 5. Results Analysis

```python
# Print formatted summary
collector.print_summary()

# Access raw results
for result in collector.results:
    print(result)

# Access errors
for error in collector.errors:
    print(error)

# Get summary dict
summary = collector.summarize()
```

## Performance Timing

Use the `timer` context manager:

```python
with dolphain.timer("My operation"):
    # Your code here
    result = expensive_computation()
# Prints: My operation: 1.234 seconds

# Access elapsed time
with dolphain.timer("Processing", verbose=False) as t:
    result = process_data()
print(f"Took {t.elapsed:.3f} seconds")
```

## Example Pipelines

### Basic Statistics

```python
def stats_pipeline(filepath):
    data = dolphain.read_ears_file(filepath)
    acoustic = data['data']

    return {
        'duration': data['duration'],
        'rms': np.sqrt(np.mean(acoustic**2)),
        'std': np.std(acoustic),
        'peak': np.max(np.abs(acoustic)),
    }
```

### Wavelet Denoising

```python
def denoise_pipeline(filepath):
    data = dolphain.read_ears_file(filepath)
    acoustic = data['data']

    original_rms = np.sqrt(np.mean(acoustic**2))
    denoised, threshold = dolphain.wavelet_denoise(
        acoustic, return_threshold=True
    )
    denoised_rms = np.sqrt(np.mean(denoised**2))

    return {
        'threshold': threshold,
        'noise_reduction_pct': (1 - denoised_rms/original_rms) * 100,
    }
```

### Multi-Wavelet Comparison

```python
def compare_wavelets(filepath):
    data = dolphain.read_ears_file(filepath)
    acoustic = data['data']

    results = {}
    for wavelet in ['db4', 'db8', 'db20']:
        denoised = dolphain.wavelet_denoise(acoustic, wavelet=wavelet)
        rms = np.sqrt(np.mean(denoised**2))
        results[f'{wavelet}_rms'] = rms

    return results
```

## Working with Results

### Convert to DataFrame

```python
import pandas as pd

df = pd.DataFrame(collector.results)
print(df.describe())
df.to_csv('results.csv', index=False)
```

### Visualize

```python
import matplotlib.pyplot as plt

df = pd.DataFrame(collector.results)
df['rms'].hist(bins=20)
plt.xlabel('RMS')
plt.ylabel('Count')
plt.show()
```

## Best Practices

1. **Use reproducible seeds** for random selection
2. **Test on small subsets** first
3. **Return consistent dict keys** from pipelines
4. **Handle edge cases** in your pipeline
5. **Monitor timing** for optimization
6. **Save results** to CSV/JSON for later analysis

## Complete Example Notebook

See `examples/batch_experiments.ipynb` for:

- Multiple experiment examples
- Visualization techniques
- Result analysis methods
- Custom pipeline templates

## Performance Tips

1. **Batch size**: Start small (10-20 files) for testing
2. **Error handling**: Let BatchProcessor catch errors
3. **Memory**: Process one file at a time (automatic)
4. **Timing**: Use `timer()` for optimization
5. **Profiling**: Check `collector.timings` for bottlenecks

## Testing

Quick test:

```python
# Find files
files = dolphain.find_data_files('data', '**/*.210')[:3]

# Simple pipeline
def test_pipeline(fp):
    data = dolphain.read_ears_file(fp)
    return {'duration': data['duration']}

# Run
processor = dolphain.BatchProcessor()
collector = processor.process_files(files, test_pipeline)
collector.print_summary()
```
