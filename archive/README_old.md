# EARS Data Reader

A Python module for reading and analyzing EARS (Ecological Acoustic Recorder) binary data files from underwater acoustic recordings in the Gulf of Mexico.

## Overview

This module provides a clean, efficient, and scientifically proper way to read and visualize EARS binary data files (`.130`, `.190`, etc.) without requiring the original `unophysics` library.

## Files

- **`ears_reader.py`** - Main module with all reading and plotting functions
- **`ears_analysis_demo.ipynb`** - Jupyter notebook demonstrating usage
- **`dolphain.ipynb`** - Original development notebook (contains inline code)

## Installation

### Dependencies

```bash
pip install numpy matplotlib scipy
```

The module uses only standard scientific Python libraries:

- `numpy` - Numerical array operations
- `matplotlib` - Plotting and visualization
- `scipy` - Signal processing (spectrograms)
- Standard library: `struct`, `datetime`, `pathlib`

### Usage

Simply import the module (ensure `ears_reader.py` is in your Python path or working directory):

```python
import ears_reader
```

## Quick Start

```python
import ears_reader
from pathlib import Path

# Read a data file
file_path = Path('path/to/your/file.190')
data = ears_reader.read_ears_file(file_path)

# Display file information
ears_reader.print_file_info(data, file_path)

# Create visualizations
ears_reader.plot_waveform(data)
ears_reader.plot_spectrogram(data, fmax=5000)
ears_reader.plot_overview(data, fmax=5000, xlim_zoom=(5, 10))
```

## API Reference

### `read_ears_file(filepath, normalize=False)`

Read an EARS binary data file.

**Parameters:**

- `filepath` (str or Path): Path to the EARS data file
- `normalize` (bool, optional): If True, normalize data to [-1, 1] range

**Returns:**

- `dict` containing:
  - `data`: numpy array of acoustic samples
  - `fs`: sampling rate (192,000 Hz)
  - `time_start`: datetime of recording start
  - `time_end`: datetime of recording end
  - `timestamps`: list of timestamps from headers
  - `duration`: duration in seconds
  - `n_samples`: number of samples

### `plot_waveform(ears_data, xlim=None, figsize=(16, 6))`

Plot the acoustic waveform in time domain.

**Parameters:**

- `ears_data` (dict): Dictionary returned by `read_ears_file()`
- `xlim` (tuple, optional): Time limits (start, end) in seconds
- `figsize` (tuple, optional): Figure size (width, height)

### `plot_spectrogram(ears_data, fmax=None, nperseg=1024, noverlap=512, figsize=(16, 6), cmap='nipy_spectral', vmin=None, vmax=None)`

Plot a spectrogram of the acoustic data.

**Parameters:**

- `ears_data` (dict): Dictionary returned by `read_ears_file()`
- `fmax` (float, optional): Maximum frequency to display (Hz)
- `nperseg` (int, optional): Length of each segment for FFT
- `noverlap` (int, optional): Number of points to overlap between segments
- `figsize` (tuple, optional): Figure size
- `cmap` (str, optional): Colormap name
- `vmin`, `vmax` (float, optional): Min and max values for color scale (dB)

### `plot_overview(ears_data, fmax=None, xlim_zoom=None, figsize=(16, 12))`

Create a multi-panel overview plot with waveform and spectrogram.

**Parameters:**

- `ears_data` (dict): Dictionary returned by `read_ears_file()`
- `fmax` (float, optional): Maximum frequency to display (Hz)
- `xlim_zoom` (tuple, optional): Time limits for zoomed waveform (seconds)
- `figsize` (tuple, optional): Figure size

### `print_file_info(ears_data, filepath=None)`

Print a formatted summary of file information.

**Parameters:**

- `ears_data` (dict): Dictionary returned by `read_ears_file()`
- `filepath` (str or Path, optional): File path for display

## EARS File Format

The EARS binary format uses the following structure:

- **Record size**: 512 bytes per record
- **Header size**: 12 bytes per record
- **Data per record**: 250 samples (16-bit signed integers, big-endian)
- **Sampling rate**: 192,000 Hz
- **Timestamp sampling rate**: 32,000 Hz
- **Epoch**:
  - Files starting with '7': October 27, 2015
  - Other files: January 1, 2000

## Examples

### Basic Usage

```python
import ears_reader
from pathlib import Path

# Read file
data = ears_reader.read_ears_file('sample_data/71621DC7.190')

# Print information
print(f"Duration: {data['duration']:.2f} seconds")
print(f"Recorded: {data['time_start']}")

# Plot waveform
ears_reader.plot_waveform(data)
```

### Advanced Spectrogram

```python
# High-resolution spectrogram
ears_reader.plot_spectrogram(
    data,
    fmax=8000,
    nperseg=2048,  # Better frequency resolution
    noverlap=1536,  # Smoother time resolution
    cmap='viridis'
)
```

### Normalized Data

```python
# Read with normalization
data_norm = ears_reader.read_ears_file('sample.190', normalize=True)
print(f"Mean: {np.mean(data_norm['data']):.6f}")  # Close to 0
print(f"Max: {np.max(np.abs(data_norm['data'])):.6f}")  # Close to 1
```

### Custom Analysis

```python
# Access raw data for custom analysis
import numpy as np

data = ears_reader.read_ears_file('sample.190')
acoustic = data['data']

# Compute statistics
rms = np.sqrt(np.mean(acoustic**2))
peak = np.max(np.abs(acoustic))
print(f"RMS: {rms:.2f}, Peak: {peak:.2f}")
```

## Sample Data

Sample files are included in the repository:

- `unophysics/sample_data/71621DC7.190`
- `fourier_examples/data/7164403B.130`

## Performance

The module is optimized for efficiency:

- Binary parsing using `struct` module
- NumPy arrays for fast numerical operations
- SciPy spectrograms for professional-grade signal processing

Typical performance on a modern laptop:

- Reading ~21 seconds of data: ~150-200 ms
- Generating spectrogram: ~5-6 seconds

## License

Extracted from the `unophysics` library originally written by the user. This module provides a standalone implementation for reading EARS data files.

## Acknowledgments

- Original EARS file format implemented in the `unophysics` library
- Gulf of Mexico acoustic recordings from EARS (Ecological Acoustic Recorder) system
- SciPy and NumPy communities for excellent scientific computing tools

## Support

For issues or questions, refer to:

- The demo notebook: `ears_analysis_demo.ipynb`
- The original notebook: `dolphain.ipynb`
- Function docstrings in `ears_reader.py`
