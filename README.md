# 🐬 Dolphain - Dolphin Acoustic Analysis Library

**Interactive Showcase:** https://dolphain.mantilabs.ai/showcase.html 🎵
**Web Portal:** https://dolphain.mantilabs.ai/portal/index.html 💻

A Python library for analyzing underwater acoustic data from EARS (Embedded Acoustic Recording System) files, with focus on dolphin vocalization detection and characterization.
![Status](https://img.shields.io/badge/status-production-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🎯 What Is This?

**Mission:** Analyze 949,504 underwater acoustic recordings to detect and understand dolphin communication patterns.

**Innovation:** 6-feature "interestingness" scoring system that goes beyond simple whistle counting:

- Activity level (RMS energy)
- Spectral diversity (frequency range)
- Signal-to-noise ratio
- Complexity (zero-crossings)
- Temporal patterns (autocorrelation)
- Overlapping signals

**Output:** Interactive web showcase of the most interesting recordings with professional audio players featuring click-to-seek, waveform visualization, and raw/denoised audio switching.

---

## 🎨 Interactive Showcase & Portal

**Web Portal (New!):** https://dolphain.mantilabs.ai/portal/index.html

- 💻 Run Python code directly in your browser
- 📡 Fetch data from HuggingFace instantly
- 📊 Generate spectrograms and waveforms on the fly
- 🚫 No installation required

**Showcase:** https://dolphain.mantilabs.ai/showcase.html

Features:

- 🎵 Top-ranked recordings with professional audio players
- 🖱️ Click spectrograms/waveforms to seek through audio
- 🔄 Toggle between raw and denoised audio
- 📊 Visual spectrograms and waveform plots
- ⏱️ Timeline scrubber with synchronized playback
- 🎨 Dark theme with cyan accents

**Quick local test:**

```bash
cd site && python3 -m http.server 8000
# Open: http://localhost:8000/showcase.html
```

**Note:** Currently features 2 test files. Regenerate with 10-20 files when external drive is available.

---

## 🗺️ Roadmap & Future

Curious about where we're going? Check out our [ROADMAP.md](ROADMAP.md) to see our plans for advanced classification, cloud scaling, and community science.

## 🎓 Learn & Explore

We believe in learning by doing.

- **[Dolphain Studio](https://dolphain.mantilabs.ai/portal/index.html)**: Run real Python analysis code in your browser. No installation required. Includes interactive examples for denoising and detection.
- **[Showcase](https://dolphain.mantilabs.ai/showcase/index.html)**: Listen to the best signals we've found so far.

## 🛠️ Installation

```bash
git clone https://github.com/micha2718l/dolphain.git
cd dolphain
pip install -e .
```

**Requirements:**

- Python 3.8+
- NumPy, SciPy, Matplotlib
- PyWavelets (for denoising)
- Pandas (for batch processing)

---

## 🚀 Quick Start

### Super Easy - HuggingFace Integration 🎉

```python
import dolphain

# Load a random file from HuggingFace - just one line!
ears = dolphain.EARS()

# Analyze it
ears.plot('denoising', fmax=50000)
whistles = ears.detect_whistles()
print(f"Found {len(whistles)} whistles in {ears.filename}")
```

### 🕰️ Time-Based Data Access (New!)

Forget about files. Just ask for the time range you want.

```python
from dolphain import getData, build_catalog
import datetime

# 1. Index the dataset (run once)
build_catalog()

# 2. Get 10 seconds of audio, even if it crosses file boundaries
start = datetime.datetime(2017, 6, 28, 0, 20, 51)
data = getData("GoMRI-17", start, 10.0)
```

See [DATA_ACCESS.md](DATA_ACCESS.md) for full details.

### 📚 Built-in Catalog (Fastest Start!)

No need to build a catalog or download anything! Dolphain comes with a built-in catalog of 1000 sample files:

```python
from dolphain.catalog import Catalog
import pandas as pd

# Load the built-in catalog (no arguments needed!)
catalog = Catalog()
print(f"Loaded {len(catalog.df)} files")

# Query for a specific time range
start = pd.to_datetime("2017-06-28 00:30:00")
end = pd.to_datetime("2017-06-28 01:00:00")
files = catalog.query(start, end)
print(f"Found {len(files)} files in that time range")

# You can still use your own catalog if you have one
my_catalog = Catalog("path/to/my/catalog.csv")
```

The built-in catalog will be expanded as more files are added to HuggingFace.

**New!** Seamlessly fetch and analyze files from HuggingFace without any setup. See [HUGGINGFACE_INTEGRATION.md](HUGGINGFACE_INTEGRATION.md) for full documentation.

### Traditional - Local Files

```python
import dolphain

# Read EARS file (192 kHz underwater recordings)
data = dolphain.read_ears_file('sample.210')

# Or use the EARS class
ears = dolphain.EARS('sample.210')

# Denoise using wavelets (db20)
clean = dolphain.wavelet_denoise(data['data'])

# Detect whistles
whistles = dolphain.detect_whistles(clean, data['fs'])

print(f"Found {len(whistles)} dolphin whistles!")

# Plot with the EARS class
ears.plot('denoising', fmax=50000)
```

### Generate Interactive Showcase

```bash
# Activate environment
source .venv/bin/activate

# Generate showcase from analysis results
python scripts/generate_showcase.py \
  --checkpoint quick_find_results/results.json \
  --top 10 \
  --output-dir site/showcase

# Test locally
cd site && python3 -m http.server 8000
# Open: http://localhost:8000/showcase.html

# Deploy to GitHub Pages
git add site/showcase/ && git commit -m "Update showcase" && git push
```

**Note:** Showcase generation requires EARS files on external drive. Performance: ~3.6s per file.

---

## 📂 Project Structure

```
dolphain/
├── dolphain/                      # Core library package
│   ├── io.py                     # EARS file reading (192kHz data)
│   ├── signal.py                 # Wavelet denoising, whistle detection
│   ├── plotting.py               # 6-panel analysis plots
│   └── batch.py                  # Batch processing with checkpointing
│
├── scripts/                       # Command-line tools
│   ├── generate_showcase_local.py # Generate showcase (optimized)
│   ├── copy_top_files.py         # Copy top N files locally
│   ├── convert_to_mp3.py         # WAV→MP3 conversion (98% reduction)
│   └── export_top_files.py       # Export with visualizations
│
├── site/                          # GitHub Pages website
│   ├── showcase.html             # Interactive gallery with audio players
│   ├── index.html                # Landing page
│   └── showcase/                 # Generated assets
│       ├── audio/                # 66 MP3 files (21 MB total)
│       ├── images/               # 46 PNG visualizations
│       └── showcase_data.json    # Metadata for 23 files
│
├── data/                          # EARS acoustic data
│   └── Buoy210_100300_100399/    # 100 sample files
│
├── examples/                      # Jupyter notebooks
│   ├── ears_analysis_demo.ipynb  # Basic analysis demo
│   ├── batch_experiments.ipynb   # Batch processing examples
│   └── wavelet_demo.ipynb        # Denoising techniques
│
└── tests/                         # Unit tests
    └── test_ears_reader.py
```

---

## 🔬 Core Features

### 1. EARS File Reading

```python
data = dolphain.read_ears_file('recording.210')
# Returns: {
#   'data': numpy array of audio samples,
#   'fs': 192000 (sampling rate),
#   'time': time vector in seconds
# }
```

### 2. Wavelet Denoising

```python
# Remove background noise while preserving dolphin calls
clean = dolphain.wavelet_denoise(
    data['data'],
    wavelet='db20',      # Daubechies 20 wavelet
    level=5,             # Decomposition depth
    threshold_scale=2.0  # Noise threshold multiplier
)
```

### 3. Whistle Detection

```python
# Detect dolphin whistles (2-20 kHz narrow-band FM signals)
whistles = dolphain.detect_whistles(
    clean,
    fs=192000,
    freq_range=(2000, 20000),  # Whistle frequency range
    duration_threshold=0.5      # Minimum duration in seconds
)
```

### 4. Analysis Plotting

```python
# Create comprehensive 6-panel visualization:
# - Raw signal
# - Denoised signal
# - Raw spectrogram
# - Denoised spectrogram
# - Frequency spectrum
# - Detected whistles
dolphain.plot_analysis(data['data'], clean, data['fs'], data['time'])
```

### 5. Wavelet Decomposition Visualization

```python
# Visualize wavelet decomposition levels
# Shows how signal is broken down into frequency bands
dolphain.plot_wavelet_decomposition(
    data['data'],
    duration=10,         # Plot first 10 seconds
    start_offset=5,      # Start at 5 seconds
    wavelet='db20',      # Wavelet type
    level=5              # Decomposition levels
)
```

### 6. Save Audio as WAV

```python
# Save audio data for playback or further analysis
dolphain.save_wav(data['data'], 'output.wav')

# Works with stitched data from getData
audio_data = dolphain.getData("GoMRI-17", start_time, 30.0)
dolphain.save_wav(audio_data, 'stitched_audio.wav')

# Or use EARS class method
ears = dolphain.EARS()
ears.save_wav('recording.wav')
```

### 7. Batch Processing

```python
from dolphain.batch import BatchProcessor

# Process hundreds of files with progress tracking
processor = BatchProcessor(
    file_list=files,
    checkpoint_file='checkpoint.pkl'
)

results = processor.process_batch(
    process_function=analyze_file,
    batch_size=50,
    n_workers=4
)
```

---

## 🎓 Scientific Background

### EARS Data Format

- **Sampling Rate:** 192 kHz (captures up to 96 kHz by Nyquist theorem)
- **Bit Depth:** 16-bit signed integers, big-endian
- **Source:** Gulf of Mexico underwater acoustic monitoring buoys
- **Coverage:** Perfect for dolphin whistles (2-20 kHz), good for mid-frequency clicks

### Dolphin Acoustics

**Whistles (Communication):**

- Frequency: 2-20 kHz (narrow-band FM signals)
- Duration: 0.5-1.5 seconds typical
- Function: Social communication, individual identification
- Types: Signature whistles (unique IDs), pulsed calls (social contexts)
- Notable: Dolphins remember signature whistles for 20+ years

**Clicks (Echolocation):**

- Frequency: >110 kHz, often >220 kHz at peak
- Purpose: Navigation, prey detection, object recognition
- Duration: Microseconds to milliseconds
- Pattern: Rapid click trains ending in "terminal buzz" (200+ clicks/sec)

### Denoising Technique

- **Method:** Wavelet decomposition using Daubechies 20 (db20) wavelet
- **Why:** Wavelets preserve transient signals while removing stationary noise
- **Threshold:** Adaptive based on noise floor estimation
- **Result:** Clean dolphin calls without distortion

---

## 📊 Performance Stats

- **Showcase Generation:** ~13 seconds per file (5x faster than original)
- **File Optimization:** 98% reduction (1,031 MB WAV → 21 MB MP3)
- **Batch Processing:** Checkpoint-based resumable processing
- **Analysis Speed:** ~0.16 seconds per file on modern hardware

---

## 🎯 Use Cases

1. **Marine Biology Research:** Analyze dolphin communication patterns
2. **Acoustic Ecology:** Study underwater soundscapes
3. **Signal Processing:** Demonstrate wavelet denoising techniques
4. **Data Visualization:** Create interactive audio showcases
5. **Education:** Teach acoustic analysis and Python signal processing

---

## 📖 Documentation

- **`START_HERE.md`** - Quick start guide and current status
- **`HANDOFF_NOTES.md`** - Complete technical handoff documentation
- **`SHOWCASE_GUIDE.md`** - How to generate and customize showcases
- **`ENHANCED_SCORING.md`** - Details on the 6-feature scoring algorithm
- **`GITHUB_PAGES_DEPLOYMENT.md`** - Deployment workflow

---

## 🛠️ Command Reference

```bash
# Environment setup
source .venv/bin/activate

# Showcase workflow
python scripts/copy_top_files.py --checkpoint /path/to/checkpoint.pkl --top 25
python scripts/generate_showcase_local.py --output-dir site/showcase
python scripts/convert_to_mp3.py --showcase-dir site/showcase

# Local testing
cd site && python -m http.server 8003

# Deployment
git add site/showcase/ && git commit -m "Update showcase" && git push

# Utility
lsof -ti:8003 | xargs kill -9  # Kill local server
```

---

## 🤝 Contributing

This is a research project focused on dolphin acoustic analysis. Contributions welcome for:

- Additional detection algorithms (click detection, call classification)
- Performance optimizations
- Visualization enhancements
- Documentation improvements

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **Data Source:** Gulf of Mexico EARS buoy recordings
- **Inspiration:** Marine biology research and dolphin communication studies
- **Tools:** NumPy, SciPy, Matplotlib, PyWavelets

---

## 📞 Contact

**Repository:** https://github.com/micha2718l/dolphain  
**Live Demo:** https://dolphain.mantilabs.ai/showcase.html

---

**Status:** ✅ Production-ready interactive showcase with professional audio player  
**Last Updated:** October 12, 2025

_For technical details and continuation, see `HANDOFF_NOTES.md`_ 📖
