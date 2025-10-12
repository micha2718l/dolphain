# 🐬 Dolphain - Dolphin Acoustic Analysis Library# Dolphain - Underwater Acoustic Data Analysis# Dolphain - Underwater Acoustic Data Analysis# EARS Data Reader



A Python library for analyzing underwater acoustic data from EARS (Embedded Acoustic Recording System) files, with focus on dolphin vocalization detection and characterization.A Python package for reading and analyzing EARS (Ecological Acoustic Recorder) binary data files from underwater acoustic recordings in the Gulf of Mexico.



## 📦 Quick Installation## OverviewA Python package for reading and analyzing EARS (Ecological Acoustic Recorder) binary data files from underwater acoustic recordings in the Gulf of Mexico.A Python module for reading and analyzing EARS (Ecological Acoustic Recorder) binary data files from underwater acoustic recordings in the Gulf of Mexico.



```bashDolphain provides a clean, efficient, and scientifically rigorous toolkit for underwater acoustic data analysis, with a focus on EARS format files and wavelet-based denoising techniques.

git clone https://github.com/micha2718l/dolphain.git

cd dolphain## Project Structure## Overview## Overview

pip install -e .

```````



## 🚀 5-Minute Quick Startdolphain/



### Analyze One File├── dolphain/              # Main packageDolphain provides a clean, efficient, and scientifically rigorous toolkit for underwater acoustic data analysis, with a focus on EARS format files and wavelet-based denoising techniques.This module provides a clean, efficient, and scientifically proper way to read and visualize EARS binary data files (`.130`, `.190`, etc.) without requiring the original `unophysics` library.

```python

import dolphain│   ├── __init__.py       # Package initialization



# Read EARS file│   ├── io.py             # File I/O functions

data = dolphain.read_ears_file('sample.210')

│   ├── signal.py         # Signal processing (wavelet denoising)

# Denoise and detect whistles

clean = dolphain.wavelet_denoise(data['data'])│   ├── plotting.py       # Visualization functions## Project Structure## Files

whistles = dolphain.detect_whistles(clean, data['fs'])

│   └── batch.py          # Batch processing framework

print(f"Found {len(whistles)} whistles!")

```├── examples/              # Example Jupyter notebooks



### Find Interesting Files│   ├── ears_analysis_demo.ipynb

```bash

# Analyze 1000 random files (~20 minutes)│   ├── wavelet_demo.ipynb```- **`ears_reader.py`** - Main module with all reading and plotting functions

python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000

```│   └── batch_experiments.ipynb



### Listen to a File├── tests/                 # Test filesdolphain/- **`ears_analysis_demo.ipynb`** - Jupyter notebook demonstrating usage

```bash

# Convert to WAV (raw + denoised versions)│   └── test_ears_reader.py

python scripts/ears_to_wav.py filename.210

```├── ears_cli.py           # Command-line interface├── dolphain/              # Main package- **`dolphain.ipynb`** - Original development notebook (contains inline code)



## 📁 Project Organization├── ears_reader.py        # Legacy module (for compatibility)



```├── README.md│   ├── __init__.py       # Package initialization

dolphain/

├── dolphain/              # 📦 Core library├── BATCH_PROCESSING.md   # Batch processing guide

│   ├── io.py             #    EARS file reading

│   ├── signal.py         #    Signal processing & whistle detection└── requirements.txt│   ├── io.py             # File I/O functions## Installation

│   ├── plotting.py       #    Visualization utilities

│   ├── batch.py          #    Batch processing framework````

│   └── experiments.py    #    Pre-built analysis pipelines

││ ├── signal.py # Signal processing (wavelet denoising)

├── scripts/              # 🔧 Analysis tools

│   ├── quick_find.py            # Fast file finder (1000 files in 20min)## Installation

│   ├── find_interesting_files.py # 3-stage filtering (100K files)

│   ├── batch_experiments.py     # Full experiment suite│ └── plotting.py # Visualization functions### Dependencies

│   ├── visualize_random.py      # Create spectrograms

│   ├── ears_to_wav.py           # Convert to audio### Dependencies

│   └── explore_interesting.py   # Visualization reports

│├── examples/ # Example Jupyter notebooks

├── outputs/              # 📊 Generated files (not in git)

│   ├── audio/           # WAV conversions````bash

│   ├── plots/           # PNG visualizations

│   ├── results/         # CSV/JSON datapip install -r requirements.txt│   ├── ears_analysis_demo.ipynb```bash

│   └── ears_files_list.txt    # Master file list

│````

├── examples/             # 📓 Jupyter tutorials

├── tests/               # 🧪 Unit tests│ └── wavelet_demo.ipynbpip install numpy matplotlib scipy

├── docs/                # 📖 Documentation

└── data/                # 🗂️ Sample filesRequired packages:

```

- `numpy` - Numerical array operations├── tests/ # Test files```

## 🎯 Main Features

- `matplotlib` - Plotting and visualization

| Feature | Script | Time (1000 files) |

|---------|--------|-------------------|- `scipy` - Signal processing (spectrograms)│ └── test_ears_reader.py

| Find interesting files | `quick_find.py` | ~20 min |

| Visualize files | `visualize_random.py` | ~2 min |- `pywt` (PyWavelets) - Wavelet transforms for denoising

| Convert to audio | `ears_to_wav.py` | ~2 sec/file |

| Full experiments | `batch_experiments.py` | ~30 min |├── ears_cli.py # Command-line interfaceThe module uses only standard scientific Python libraries:

| Deep analysis | `find_interesting_files.py` | ~2 hours |

### Usage

## 📊 Common Tasks

├── ears_reader.py # Legacy module (for compatibility)

### 1. Find the Best Files

```bash```python

python scripts/quick_find.py \

  --file-list outputs/ears_files_list.txt \import dolphain├── README.md- `numpy` - Numerical array operations

  --n-files 1000

```

# Results in: outputs/results/quick_find_results/top_20_files.txt

```└── requirements.txt- `matplotlib` - Plotting and visualization



### 2. Visualize Files## Quick Start

```bash

# Random files from dataset```- `scipy` - Signal processing (spectrograms)

python scripts/visualize_random.py \

  --file-list outputs/ears_files_list.txt \### 1. Basic File Reading

  --n-files 5

- Standard library: `struct`, `datetime`, `pathlib`

# Results in: outputs/plots/sanity_check_plots/

``````````python



### 3. Convert to Audioimport dolphain## Installation

```bash

# Just the filenamefrom pathlib import Path

python scripts/ears_to_wav.py 72146FB7.171

### Usage

# Or full path

python scripts/ears_to_wav.py /path/to/file.210# Read a data file



# Results in: outputs/audio/data = dolphain.read_ears_file('path/to/file.190')### Dependencies

```



### 4. Batch Processing

```python# Display file informationSimply import the module (ensure `ears_reader.py` is in your Python path or working directory):

from dolphain import WhistleDetectionPipeline, run_experiment

dolphain.print_file_info(data)

pipeline = WhistleDetectionPipeline(denoise=True)

results = run_experiment(``````bash

    name="My Analysis",

    pipeline=pipeline,

    data_dir="data/",

    n_files=100### 2. Visualizationpip install -r requirements.txt```python

)



results.to_dataframe().to_csv('outputs/results/my_results.csv')

``````python```import ears_reader



## 📖 Documentation# Plot waveform



| Document | Description |dolphain.plot_waveform(data, xlim=(5, 10))```

|----------|-------------|

| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Command cheat sheet |

| **[LARGE_SCALE_ANALYSIS.md](LARGE_SCALE_ANALYSIS.md)** | Complete pipeline walkthrough |

| **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** | System design & workflows |# Plot spectrogramRequired packages:

| **[TESTING_FRAMEWORK.md](TESTING_FRAMEWORK.md)** | Testing & experiment guide |

| **[examples/](examples/)** | Jupyter notebook tutorials |dolphain.plot_spectrogram(data, fmax=5000)



## 🧪 Testing- `numpy` - Numerical array operations## Quick Start



```bash# Create comprehensive overview

pytest tests/                    # All tests

pytest tests/test_batch.py -v   # Specific filedolphain.plot_overview(data, fmax=5000, xlim_zoom=(5, 10))- `matplotlib` - Plotting and visualization

pytest --cov=dolphain           # With coverage

``````````



## 💡 Tips- `scipy` - Signal processing (spectrograms)```python



### Working with Large Datasets### 3. Wavelet Denoising

```bash

# Always use pre-generated file list (much faster!)- `pywt` (PyWavelets) - Wavelet transforms for denoisingimport ears_reader

python scripts/quick_find.py --file-list outputs/ears_files_list.txt

````python

# Sample first to test

python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 100# Denoise acoustic datafrom pathlib import Path



# Resume if interruptedacoustic_data = data['data']

python scripts/find_interesting_files.py --file-list outputs/ears_files_list.txt --resume

```denoised = dolphain.wavelet_denoise(acoustic_data)### Usage



### Output Organization

All scripts automatically save to `outputs/`:

- Audio files → `outputs/audio/`# Compare original and denoised# Read a data file

- Plots → `outputs/plots/`

- Results → `outputs/results/`dolphain.plot_denoising_comparison(data, fmax=5000)

- Analysis runs → `outputs/analysis_runs/`

```pythonfile_path = Path('path/to/your/file.190')

### File List Format

The `ears_files_list.txt` file contains one absolute path per line:# Try different wavelets

```

/Volumes/drive/Buoy200/71630000.200dolphain.plot_wavelet_comparison(import dolphaindata = ears_reader.read_ears_file(file_path)

/Volumes/drive/Buoy200/71630001.200

...    data,

```

    wavelets=['db4', 'db8', 'db20', 'sym8'],```

## 🎓 Example Results

    xlim=(5, 10)

From 100 random files:

- **70%** had dolphin whistles)# Display file information

- **23.66** mean whistles per file

- **84.5/100** top score````

- **~1.4s** processing time per file

## Quick Startears_reader.print_file_info(data, file_path)

## 🛠️ Development

### 4. Batch Processing

```bash

pip install -e ".[dev]"    # Install dev dependencies````python

black dolphain/            # Format code

flake8 dolphain/          # Lint# Define analysis pipeline### Basic File Reading and Visualization# Create visualizations

pytest tests/             # Run tests

```def my_pipeline(filepath):



## 📞 Support    data = dolphain.read_ears_file(filepath)ears_reader.plot_waveform(data)



- **Issues:** [GitHub Issues](https://github.com/micha2718l/dolphain/issues)    return {

- **Docs:** See `docs/` folder

- **Examples:** See `examples/` folder        'duration': data['duration'],```pythonears_reader.plot_spectrogram(data, fmax=5000)



---        'rms': np.sqrt(np.mean(data['data']**2))



Made with 🐬 for marine acoustic research    }import dolphainears_reader.plot_overview(data, fmax=5000, xlim_zoom=(5, 10))




# Find and select filesfrom pathlib import Path```

files = dolphain.find_data_files('data', '**/*.210')

subset = dolphain.select_random_files(files, n=10, seed=42)



# Process batch# Read a data file## API Reference

processor = dolphain.BatchProcessor(verbose=True)

collector = processor.process_files(subset, my_pipeline)data = dolphain.read_ears_file('path/to/file.190')

collector.print_summary()

```### `read_ears_file(filepath, normalize=False)`



**See [BATCH_PROCESSING.md](BATCH_PROCESSING.md) for complete batch processing guide.**# Display file information



## Featuresdolphain.print_file_info(data)Read an EARS binary data file.



### File I/O

- **`read_ears_file()`** - Read EARS binary files (.130, .190, .210, etc.)

- **`print_file_info()`** - Display file metadata# Create overview plot**Parameters:**



### Signal Processingdolphain.plot_overview(data, fmax=5000, xlim_zoom=(5, 10))

- **`wavelet_denoise()`** - Wavelet-based denoising using Universal Threshold (VisuShrink)

- **`threshold()`** - Soft/hard thresholding```- `filepath` (str or Path): Path to the EARS data file

- **`thresh_wave_coeffs()`** - Apply thresholding to wavelet coefficients

- `normalize` (bool, optional): If True, normalize data to [-1, 1] range

### Visualization

- **`plot_waveform()`** - Time-domain waveform### Wavelet Denoising

- **`plot_spectrogram()`** - Frequency-domain spectrogram

- **`plot_overview()`** - Multi-panel comprehensive view**Returns:**

- **`plot_denoising_comparison()`** - Compare original vs denoised

- **`plot_wavelet_comparison()`** - Compare different wavelet types```python



### Batch Processing# Denoise acoustic data- `dict` containing:

- **`find_data_files()`** - Discover data files by pattern

- **`select_random_files()`** - Random subset selection with seedacoustic_data = data['data']  - `data`: numpy array of acoustic samples

- **`BatchProcessor`** - Process multiple files with pipelines

- **`ResultCollector`** - Aggregate results and statisticsdenoised = dolphain.wavelet_denoise(acoustic_data)  - `fs`: sampling rate (192,000 Hz)

- **`timer`** - Context manager for performance timing

  - `time_start`: datetime of recording start

## Examples

# Compare original and denoised  - `time_end`: datetime of recording end

See the `examples/` directory for comprehensive Jupyter notebooks:

dolphain.plot_denoising_comparison(data, fmax=5000)  - `timestamps`: list of timestamps from headers

- **`ears_analysis_demo.ipynb`** - Basic EARS file reading and visualization

- **`wavelet_demo.ipynb`** - Comprehensive wavelet denoising tutorial  - `duration`: duration in seconds

- **`batch_experiments.ipynb`** - Batch processing and experiment framework
- **`dolphin_communication_analysis.ipynb`** - Ongoing dolphin click/whistle research featuring runtime guardrails, special-file comparisons, and threshold sweeps (CSV outputs saved under `reports/`).

# Try different wavelets  - `n_samples`: number of samples

## Command-Line Interface

dolphain.plot_wavelet_comparison(

Quick analysis from the command line:

    data, ### `plot_waveform(ears_data, xlim=None, figsize=(16, 6))`

```bash

# Basic usage    wavelets=['db4', 'db8', 'db20', 'sym8'],

python ears_cli.py path/to/file.190

    xlim=(5, 10)Plot the acoustic waveform in time domain.

# With options

python ears_cli.py path/to/file.190 --fmax 5000 --normalize)



# Different plot types```**Parameters:**

python ears_cli.py path/to/file.190 --plot spectrogram --fmax 8000

````

## Testing## Features- `ears_data` (dict): Dictionary returned by `read_ears_file()`

Run the test suite to verify installation:- `xlim` (tuple, optional): Time limits (start, end) in seconds

```bash### File I/O- `figsize` (tuple, optional): Figure size (width, height)

cd tests

python test_ears_reader.py- **`read_ears_file()`** - Read EARS binary files (.130, .190, etc.)

````

- **`print_file_info()`** - Display file metadata### `plot_spectrogram(ears_data, fmax=None, nperseg=1024, noverlap=512, figsize=(16, 6), cmap='nipy_spectral', vmin=None, vmax=None)`

## API Reference



### Reading Files

### Signal ProcessingPlot a spectrogram of the acoustic data.

```python

data = dolphain.read_ears_file(filepath, normalize=False)- **`wavelet_denoise()`** - Wavelet-based denoising using Universal Threshold (VisuShrink)

````

- **`threshold()`** - Soft/hard thresholding**Parameters:**

Returns a dictionary with:

- `data`: numpy array of acoustic samples- **`thresh_wave_coeffs()`** - Apply thresholding to wavelet coefficients

- `fs`: sampling rate (192000 Hz)

- `time_start`: datetime of recording start- `ears_data` (dict): Dictionary returned by `read_ears_file()`

- `time_end`: datetime of recording end

- `timestamps`: list of timestamps from headers### Visualization- `fmax` (float, optional): Maximum frequency to display (Hz)

- `duration`: duration in seconds

- `n_samples`: number of samples- **`plot_waveform()`** - Time-domain waveform- `nperseg` (int, optional): Length of each segment for FFT

### Wavelet Denoising- **`plot_spectrogram()`** - Frequency-domain spectrogram- `noverlap` (int, optional): Number of points to overlap between segments

```python- **`plot_overview()`** - Multi-panel comprehensive view- `figsize` (tuple, optional): Figure size

denoised = dolphain.wavelet_denoise(

    data,- **`plot_denoising_comparison()`** - Compare original vs denoised- `cmap` (str, optional): Colormap name

    wavelet='db20',

    mode='soft',- **`plot_wavelet_comparison()`** - Compare different wavelet types- `vmin`, `vmax` (float, optional): Min and max values for color scale (dB)

    level=None,

    return_threshold=False

)

```## Examples### `plot_overview(ears_data, fmax=None, xlim_zoom=None, figsize=(16, 12))`

**Parameters:**

- `data`: Input signal (1D numpy array)

- `wavelet`: Wavelet family (default: 'db20')See the `examples/` directory for comprehensive Jupyter notebooks:Create a multi-panel overview plot with waveform and spectrogram.

- `mode`: Thresholding mode ('soft' or 'hard')

- `level`: Decomposition level (None = automatic)

- `return_threshold`: If True, also return threshold value

- **`ears_analysis_demo.ipynb`** - Basic EARS file reading and visualization**Parameters:**

Uses Universal Threshold (VisuShrink method):

- Threshold = σ × √(2 × ln(N))- **`wavelet_demo.ipynb`** - Comprehensive wavelet denoising tutorial

- Noise estimation via MAD: σ = median(|coeffs|) / 0.6745

- `ears_data` (dict): Dictionary returned by `read_ears_file()`

### Batch Processing

## Command-Line Interface- `fmax` (float, optional): Maximum frequency to display (Hz)

See [BATCH_PROCESSING.md](BATCH_PROCESSING.md) for complete documentation.

- `xlim_zoom` (tuple, optional): Time limits for zoomed waveform (seconds)

````python

# Find filesQuick analysis from the command line:- `figsize` (tuple, optional): Figure size

files = dolphain.find_data_files(root_dir, pattern='**/*.210')



# Random selection

subset = dolphain.select_random_files(files, n=10, seed=42)```bash### `print_file_info(ears_data, filepath=None)`



# Create processor# Basic usage

processor = dolphain.BatchProcessor(verbose=True)

python ears_cli.py path/to/file.190Print a formatted summary of file information.

# Process files

collector = processor.process_files(files, pipeline_func)



# View results# With options**Parameters:**

collector.print_summary()

summary = collector.summarize()python ears_cli.py path/to/file.190 --fmax 5000 --normalize

````

- `ears_data` (dict): Dictionary returned by `read_ears_file()`

## EARS File Format

# Different plot types- `filepath` (str or Path, optional): File path for display

The EARS binary format uses the following structure:

python ears_cli.py path/to/file.190 --plot spectrogram --fmax 8000

- **Record size**: 512 bytes per record

- **Header size**: 12 bytes per record```## EARS File Format

- **Data per record**: 250 samples (16-bit signed integers, big-endian)

- **Sampling rate**: 192,000 Hz

- **Timestamp sampling rate**: 32,000 Hz

- **Epoch**:## TestingThe EARS binary format uses the following structure:

  - Files starting with '7': October 27, 2015

  - Other files: January 1, 2000

## Wavelet Denoising MethodRun the test suite to verify installation:- **Record size**: 512 bytes per record

Dolphain uses the **VisuShrink (Universal Threshold)** method:- **Header size**: 12 bytes per record

1. **Decomposition**: Discrete wavelet transform (DWT)```bash- **Data per record**: 250 samples (16-bit signed integers, big-endian)

2. **Noise Estimation**: Median Absolute Deviation (MAD)

   - σ = median(|detail_coeffs|) / 0.6745cd tests- **Sampling rate**: 192,000 Hz

3. **Threshold Calculation**: σ × √(2 × ln(N))

4. **Thresholding**: Soft or hard thresholding on detail coefficientspython test_ears_reader.py- **Timestamp sampling rate**: 32,000 Hz

5. **Reconstruction**: Inverse DWT

```````- **Epoch**:

**Supported Wavelets:**

- Daubechies family: db4, db8, db20 (default)  - Files starting with '7': October 27, 2015

- Symlet family: sym8

- And all other PyWavelets families## API Reference  - Other files: January 1, 2000



## Contributing



This is a research project for underwater acoustic analysis. Contributions are welcome!### Reading Files## Examples



## License



[Add your license here]```python### Basic Usage



## Contactdata = dolphain.read_ears_file(filepath, normalize=False)



[Add your contact information here]``````python



## Acknowledgmentsimport ears_reader



- EARS data format specificationReturns a dictionary with:from pathlib import Path

- PyWavelets library for wavelet transforms

- Original unophysics library for inspiration- `data`: numpy array of acoustic samples


- `fs`: sampling rate (192000 Hz)# Read file

- `time_start`: datetime of recording startdata = ears_reader.read_ears_file('sample_data/71621DC7.190')

- `time_end`: datetime of recording end

- `timestamps`: list of timestamps from headers# Print information

- `duration`: duration in secondsprint(f"Duration: {data['duration']:.2f} seconds")

- `n_samples`: number of samplesprint(f"Recorded: {data['time_start']}")



### Wavelet Denoising# Plot waveform

ears_reader.plot_waveform(data)

```python```

denoised = dolphain.wavelet_denoise(

    data,### Advanced Spectrogram

    wavelet='db20',          # Wavelet type

    thresh=None,             # Auto-calculate if None```python

    return_threshold=False,  # Return threshold value# High-resolution spectrogram

    hard_threshold=False     # Use soft thresholdingears_reader.plot_spectrogram(

)    data,

```    fmax=8000,

    nperseg=2048,  # Better frequency resolution

## Scientific Background    noverlap=1536,  # Smoother time resolution

    cmap='viridis'

### Wavelet Denoising)

```````

Implements the Universal Threshold method (VisuShrink) from:

### Normalized Data

> Donoho, D. L., & Johnstone, I. M. (1994). Ideal spatial adaptation by wavelet shrinkage. _Biometrika_, 81(3), 425-455.

````python

Key advantages for acoustic data:# Read with normalization

- Preserves transient features (clicks, pulses)data_norm = ears_reader.read_ears_file('sample.190', normalize=True)

- Adaptive to signal characteristics  print(f"Mean: {np.mean(data_norm['data']):.6f}")  # Close to 0

- Multi-resolution analysisprint(f"Max: {np.max(np.abs(data_norm['data'])):.6f}")  # Close to 1

- No phase distortion```



### EARS Format### Custom Analysis



EARS (Ecological Acoustic Recorder) files use a proprietary binary format:```python

- 512-byte records (12-byte header + 500-byte data)# Access raw data for custom analysis

- 250 samples per record (16-bit signed integers, big-endian)import numpy as np

- 192 kHz sampling rate

- Embedded timestamps in headersdata = ears_reader.read_ears_file('sample.190')

acoustic = data['data']

## License

# Compute statistics

MIT Licenserms = np.sqrt(np.mean(acoustic**2))

peak = np.max(np.abs(acoustic))

## Authorsprint(f"RMS: {rms:.2f}, Peak: {peak:.2f}")

````

Michael Haas and contributors

## Sample Data

## Acknowledgments

Sample files are included in the repository:

- University of New Orleans Physics Department

- [LADC GEMM Consortium](http://www.ladcgemm.org/)- `unophysics/sample_data/71621DC7.190`

- PyWavelets, NumPy, SciPy, and Matplotlib communities- `fourier_examples/data/7164403B.130`

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
