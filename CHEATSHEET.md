# 🐬 Dolphain Testing Framework - Cheat Sheet

## Quick Start

```bash
# Install and verify
pip install -r requirements.txt
python3 verify_framework.py

# Run tests
pytest tests/test_batch.py -v

# Try examples
jupyter notebook examples/experiment_templates.ipynb
```

## Pre-built Pipelines

### Basic Metrics

```python
import dolphain
pipeline = dolphain.BasicMetricsPipeline()
results = dolphain.run_experiment("Metrics", pipeline, n_files=20)
```

**Output:** rms, peak, dynamic_range, zero_crossing_rate

### Whistle Detection

```python
pipeline = dolphain.WhistleDetectionPipeline(denoise=True, threshold_factor=3.0)
results = dolphain.run_experiment("Whistles", pipeline, n_files=20)
```

**Output:** n_whistles, mean_duration, coverage_percent

### Spectral Analysis

```python
pipeline = dolphain.SpectralAnalysisPipeline(freq_bands={'low': (0, 5000), ...})
results = dolphain.run_experiment("Spectral", pipeline, n_files=20)
```

**Output:** band_power, peak_freq, spectral_centroid

### Denoising Comparison

```python
pipeline = dolphain.DenoisingComparisonPipeline(wavelets=['db4','db8'], levels=[3,5])
results = dolphain.run_experiment("Denoise", pipeline, n_files=20)
```

**Output:** SNR and RMS for each wavelet/level combo

## Method Comparison

```python
methods = {
    'No Denoise': dolphain.WhistleDetectionPipeline(denoise=False),
    'With Denoise': dolphain.WhistleDetectionPipeline(denoise=True),
}
results = dolphain.compare_methods("Compare", methods, n_files=20, seed=42)
```

## Custom Pipeline

```python
class MyPipeline:
    def __init__(self, param=1.0):
        self.param = param

    def __call__(self, filepath):
        data = dolphain.read_ears_file(filepath)
        # Your analysis
        return {"my_metric": value}

results = dolphain.run_experiment("Custom", MyPipeline(), n_files=10)
```

## Batch Processing (Manual)

```python
# Define pipeline
def my_pipeline(filepath):
    data = dolphain.read_ears_file(filepath)
    return {"metric": value}

# Get files
files = dolphain.find_data_files("data", "**/*.210")
subset = dolphain.select_random_files(files, n=10, seed=42)

# Process
processor = dolphain.BatchProcessor(verbose=True)
collector = processor.process_files(subset, my_pipeline)

# Results
collector.print_summary()
summary = collector.summarize()
```

## Results Analysis

```python
import pandas as pd

# To DataFrame
df = pd.DataFrame(collector.results)

# Summary stats
summary = collector.summarize()
print(summary['metrics']['my_metric']['mean'])

# Export
df.to_csv('results.csv', index=False)

import json
with open('summary.json', 'w') as f:
    json.dump(summary, f, indent=2)
```

## Testing

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_batch.py -v

# Specific test class
pytest tests/test_batch.py::TestBatchProcessor -v

# With coverage
pytest tests/ --cov=dolphain --cov-report=html
```

## File Locations

| File                                  | Purpose            |
| ------------------------------------- | ------------------ |
| `dolphain/experiments.py`             | Pipeline templates |
| `tests/test_batch.py`                 | Test suite         |
| `examples/experiment_templates.ipynb` | Tutorial           |
| `TESTING_FRAMEWORK.md`                | Complete guide     |
| `TESTING_QUICK_START.md`              | Quick reference    |

## Common Patterns

### Test on small subset first

```python
results = dolphain.run_experiment("Test", pipeline, n_files=3, verbose=True)
```

### Reproducible experiments

```python
# Always use same seed for same files
results = dolphain.run_experiment("Exp", pipeline, n_files=20, seed=42)
```

### Check for errors

```python
if collector.errors:
    for error in collector.errors:
        print(f"{error['file']}: {error['error_type']}")
```

### Access individual results

```python
for result in collector.results:
    print(f"{result['file']}: {result['my_metric']:.3f}")
```

## Tips

💡 Test pipeline on one file before batch: `result = pipeline(test_file)`  
💡 Use fixed seeds for reproducibility: `seed=42`  
💡 Start with small n_files to test: `n_files=5`  
💡 Use verbose=True for debugging: `BatchProcessor(verbose=True)`  
💡 Check summary stats: `collector.print_summary()`

## Documentation

📚 **TESTING_FRAMEWORK.md** - Complete guide with examples  
📚 **TESTING_QUICK_START.md** - Quick reference  
📚 **examples/experiment_templates.ipynb** - Interactive tutorial  
📚 **BATCH_PROCESSING.md** - Batch processing details

---

**Ready to start!** 🚀

```python
import dolphain
pipeline = dolphain.BasicMetricsPipeline()
results = dolphain.run_experiment("My First Experiment", pipeline, n_files=10)
```
