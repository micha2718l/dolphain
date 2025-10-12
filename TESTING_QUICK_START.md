# Testing and Experimentation Guide - Quick Reference

> **Full documentation:** See [TESTING_FRAMEWORK.md](TESTING_FRAMEWORK.md) for complete details.

## Running Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=dolphain --cov-report=html

# Run specific test file
pytest tests/test_batch.py -v
```

## Experiment Templates

The library includes pre-built experiment pipelines:

### 1. Basic Metrics Pipeline

```python
import dolphain

pipeline = dolphain.BasicMetricsPipeline()
results = dolphain.run_experiment(
    name="Basic Metrics",
    pipeline=pipeline,
    n_files=20
)
```

Extracts: RMS, peak amplitude, dynamic range, zero-crossing rate

### 2. Whistle Detection Pipeline

```python
pipeline = dolphain.WhistleDetectionPipeline(
    denoise=True,
    threshold_factor=3.0
)
results = dolphain.run_experiment("Whistle Detection", pipeline, n_files=20)
```

Detects and characterizes dolphin whistles

### 3. Spectral Analysis Pipeline

```python
pipeline = dolphain.SpectralAnalysisPipeline(
    freq_bands={
        'low': (0, 5000),
        'whistle': (5000, 25000),
        'high': (25000, 100000),
    }
)
results = dolphain.run_experiment("Spectral Analysis", pipeline, n_files=20)
```

Analyzes power distribution across frequency bands

### 4. Method Comparison

```python
methods = {
    'No Denoising': dolphain.WhistleDetectionPipeline(denoise=False),
    'With Denoising': dolphain.WhistleDetectionPipeline(denoise=True),
}

results = dolphain.compare_methods(
    method_name="Denoising Effect",
    pipelines=methods,
    n_files=20
)
```

## Custom Pipeline Example

```python
from pathlib import Path
from typing import Dict, Any
import dolphain
import numpy as np

class MyPipeline:
    def __init__(self, parameter=1.0):
        self.parameter = parameter

    def __call__(self, filepath: Path) -> Dict[str, Any]:
        data = dolphain.read_ears_file(filepath)
        # Your analysis here
        return {
            "my_metric": value,
            "duration": data["duration"],
        }

# Use it
pipeline = MyPipeline(parameter=2.5)
results = dolphain.run_experiment("My Experiment", pipeline, n_files=10)
results.print_summary()
```

## Interactive Examples

See `examples/experiment_templates.ipynb` for a complete tutorial with:

- All built-in pipelines demonstrated
- Visualization examples
- Custom pipeline creation
- Results export

## Batch Processing

```python
# Define a processing function
def my_pipeline(filepath):
    data = dolphain.read_ears_file(filepath)
    return {"metric": compute_something(data)}

# Find files
files = dolphain.find_data_files("data", "**/*.210")
subset = dolphain.select_random_files(files, n=10, seed=42)

# Process batch
processor = dolphain.BatchProcessor(verbose=True)
collector = processor.process_files(subset, my_pipeline)
collector.print_summary()

# Access results
import pandas as pd
df = pd.DataFrame(collector.results)
```

## Documentation Files

- **[TESTING_FRAMEWORK.md](TESTING_FRAMEWORK.md)** - Complete testing/experimentation guide
- **[BATCH_PROCESSING.md](BATCH_PROCESSING.md)** - Batch processing details
- **[examples/experiment_templates.ipynb](examples/experiment_templates.ipynb)** - Interactive tutorial
- **[examples/batch_experiments.ipynb](examples/batch_experiments.ipynb)** - Batch processing examples

## Key Features

✅ Pre-built analysis pipelines  
✅ Batch processing with progress tracking  
✅ Automatic result collection and statistics  
✅ Method comparison framework  
✅ Easy custom pipeline creation  
✅ Comprehensive unit tests  
✅ Reproducible experiments (fixed seeds)
