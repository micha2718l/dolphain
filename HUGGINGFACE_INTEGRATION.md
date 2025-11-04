# HuggingFace Integration

Dolphain now includes seamless integration with HuggingFace Datasets Hub, making it incredibly easy to access and analyze underwater acoustic data without managing local file storage.

## Installation

```bash
pip install dolphain
pip install huggingface_hub
```

## Quick Start

### The Easiest Way 🚀

```python
import dolphain

# Load a random file from HuggingFace - just one line!
ears = dolphain.EARS()

# That's it! Now analyze away
print(ears)
ears.plot('denoising', fmax=50000)
```

### Output:
```
EARS(filename='7178E5DC.200', duration=43.26s, fs=192000Hz, source='huggingface')
```

## Usage Examples

### 1. Random File (Default)

```python
import dolphain

# Get a random file from the default dataset
ears = dolphain.EARS()

# Access data
print(f"Duration: {ears.duration:.2f}s")
print(f"Audio data: {ears.data.shape}")
print(f"Sampling rate: {ears.fs} Hz")

# Show info
ears.info()
```

### 2. Specific File

```python
# Load a specific file by name
ears = dolphain.EARS(filename='7178E5DC.200')
```

### 3. Different Buoy or Dataset

```python
# Get file from BUOY210 instead of default BUOY200
ears = dolphain.EARS(data_path='2017_South/BUOY210')

# Or use a completely different dataset
ears = dolphain.EARS(
    dataset_id='YourOrg/YourDataset',
    data_path='path/to/files'
)
```

### 4. Local Files Still Work!

```python
# Load from local file system
ears = dolphain.EARS('path/to/local/file.200')
```

## Analysis with the EARS Class

The `EARS` class provides convenient methods for common operations:

### Denoising

```python
ears = dolphain.EARS()

# Apply wavelet denoising
denoised = ears.denoise(wavelet='db20')
```

### Whistle Detection

```python
ears = dolphain.EARS()

# Detect dolphin whistles
whistles = ears.detect_whistles(
    freq_range=(2000, 20000),
    min_duration=0.1
)

print(f"Found {len(whistles)} whistles")
for w in whistles:
    print(f"  {w['start_time']:.2f}s: {w['min_freq']:.0f}-{w['max_freq']:.0f} Hz")
```

### Visualization

```python
ears = dolphain.EARS()

# Different plot types
ears.plot('overview', fmax=50000)
ears.plot('waveform', xlim=(0, 10))
ears.plot('spectrogram', fmax=25000)
ears.plot('denoising', wavelet='db20', fmax=50000)
```

## Using the Function API

If you prefer working with dictionaries instead of class instances:

```python
import dolphain

# Fetch file as dictionary
data = dolphain.fetch_huggingface_file()

# Use with any dolphain function
dolphain.plot_waveform(data)
denoised = dolphain.wavelet_denoise(data['data'])
```

### Function Parameters

```python
dolphain.fetch_huggingface_file(
    dataset_id="ColorSynth/GoMRI-17",     # HuggingFace dataset
    data_path="2017_South/BUOY200",      # Path within dataset
    file_extension=".200",                # File type to fetch
    random_file=True,                     # Random selection
    filename=None,                        # Or specific file
    normalize=True,                       # Normalize audio data
    cleanup=True                          # Delete temp files
)
```

## Advanced Usage

### Keep Temporary Files

```python
# Don't delete the downloaded file (for inspection)
ears = dolphain.EARS(cleanup=False)
print(f"File saved at: {ears.metadata['temp_path']}")
```

### Batch Processing

```python
import dolphain

# Process multiple random files
for i in range(10):
    ears = dolphain.EARS()
    whistles = ears.detect_whistles()
    print(f"{ears.filename}: {len(whistles)} whistles, {ears.duration:.2f}s")
```

### Specific Analysis Pipeline

```python
import dolphain

# Load file
ears = dolphain.EARS(filename='7178E5DC.200')

# Denoise
denoised = ears.denoise(wavelet='db20', hard_threshold=False)

# Detect whistles in denoised data
# (Note: would need to create a new EARS object or modify detect_whistles)
whistles = ears.detect_whistles(
    freq_range=(3000, 18000),
    min_duration=0.2,
    power_threshold_percentile=90
)

# Visualize
ears.plot('denoising', xlim=(5, 15), fmax=20000)
```

## Default Dataset: ColorSynth/GoMRI-17

By default, `dolphain.EARS()` fetches from the **ColorSynth/GoMRI-17** dataset, which contains:

- **~1000 EARS recordings** (.200 format)
- **192 kHz sampling rate**
- **~43 seconds per file** (~8.4 MB each)
- **Gulf of Mexico buoy recordings** (2017)
- **Locations**: BUOY200, BUOY210, and others
- **Marine mammal vocalizations** including dolphins and whales

**Dataset Link**: https://huggingface.co/datasets/ColorSynth/GoMRI-17

## Class Attributes

The `EARS` class provides easy access to all metadata:

```python
ears = dolphain.EARS()

# Quick access attributes
ears.data          # Audio samples (numpy array)
ears.fs            # Sampling rate (192000 Hz)
ears.duration      # Duration in seconds
ears.time_start    # Recording start time (datetime)
ears.time_end      # Recording end time (datetime)
ears.filename      # Source filename

# Full metadata dictionary
ears.metadata      # Contains all information including:
                   # - source ('huggingface', 'local')
                   # - dataset_id
                   # - timestamps
                   # - data_path
```

## Methods

| Method | Description |
|--------|-------------|
| `ears.info()` | Print detailed file information |
| `ears.denoise(**kwargs)` | Apply wavelet denoising |
| `ears.detect_whistles(**kwargs)` | Detect dolphin whistles |
| `ears.plot(plot_type, **kwargs)` | Generate visualizations |

## Plot Types

| Type | Description |
|------|-------------|
| `'overview'` | Multi-panel view: waveform + spectrogram + zoom |
| `'waveform'` | Time-domain waveform only |
| `'spectrogram'` | Frequency-time spectrogram only |
| `'denoising'` | Compare original vs denoised (waveform + spectrogram) |

## Examples in Repository

- **`test_huggingface_ears.ipynb`** - Interactive Jupyter notebook walkthrough
- **`examples/huggingface_quick_start.py`** - Comprehensive Python script with all features

## Troubleshooting

### Import Error: huggingface_hub

```bash
pip install huggingface_hub
```

### No Files Found

Check the `data_path` parameter matches the dataset structure:

```python
# List available files first
from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_files(repo_id="ColorSynth/GoMRI-17", repo_type="dataset")
print([f for f in files if f.endswith('.200')])
```

### Authentication Required

Some HuggingFace datasets require authentication:

```bash
huggingface-cli login
```

Or in Python:
```python
from huggingface_hub import login
login()
```

## Performance Notes

- **First download**: ~8-10 seconds per file (8.4 MB)
- **Subsequent access**: Files are cached by HuggingFace
- **Memory usage**: ~350 MB per loaded file (uncompressed audio data)
- **Cleanup**: Temp files automatically deleted (unless `cleanup=False`)

## Contributing

Have a dataset you'd like to add? Suggestions for improvements? 

Open an issue or PR at: https://github.com/micha2718l/dolphain

---

**Happy analyzing! 🐬🎵**
