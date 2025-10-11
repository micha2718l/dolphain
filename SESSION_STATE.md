# Dolphain Project - Session State & Continuation Guide

**Last Updated:** October 9, 2025  
**Status:** Ready to create dolphin communication analysis notebook

## Current Location & Context

- **Working Directory:** `/Users/mjhaas/code/dolphain`
- **Active File:** `examples/batch_experiments.ipynb` (lines 38-44 selected)
- **Python Environment:** `.venv` with editable install (`dolphain-0.1.0`)
- **Repository:** unophysics (owner: micha2718l, branch: master)

## Project Mission

**PRIMARY GOAL:** Analyze underwater acoustic recordings (EARS data) to detect, classify, and understand dolphin communication through clicks and whistles. This is the core research objective - understanding dolphin "language."

## What Has Been Completed ✅

### 1. Batch Processing Framework (COMPLETE)

- **File:** `dolphain/batch.py` - Full batch experiment framework
- **Features:**
  - `BatchProcessor` class with timing and progress tracking
  - `BatchExperiment` class for organizing experiments
  - Pipeline execution with error handling
  - Performance metrics and reporting
- **Tested:** Successfully ran on 3 files (100% success rate, ~0.16s per file)
- **Documentation:**
  - `BATCH_PROCESSING.md` - User guide
  - `BATCH_IMPLEMENTATION.md` - Technical details
  - `examples/batch_experiments.ipynb` - Demo notebook

### 2. Package Development Setup (COMPLETE)

- **File:** `setup.py` - Created for editable installation
- **Status:** Package installed with `pip install -e .`
- **Verification:** All 15 functions accessible via `import dolphain`
- **Fixed:** `dolphain/__init__.py` with `__version__ = "0.1.0"`
- **Documentation:** `DEVELOPMENT_INSTALL.md` - Installation guide

### 3. Dependencies Installed (COMPLETE)

- Core: NumPy, SciPy, Matplotlib, PyWavelets
- New: Pandas (for DataFrame operations)
- All requirements satisfied

### 4. Research Completed (COMPLETE)

Extensive research on dolphin acoustics retrieved from Wikipedia:

**Dolphin Clicks (Echolocation):**

- Frequency: >110 kHz, often >220 kHz at peak
- Purpose: Navigation, prey detection, object recognition
- Duration: Very brief (microseconds to milliseconds)
- Pattern: Rapid click trains, ending in "terminal buzz" (200+ clicks/sec)
- Detection: Requires high sampling rate (>220 kHz optimal)
- Our EARS data: 192 kHz sampling (Nyquist = 96 kHz) - **can detect clicks up to 96 kHz**

**Dolphin Whistles (Communication):**

- Frequency: Typically 2-20 kHz (narrow-band FM signals)
- Duration: 0.5-1.5 seconds typical
- Types:
  - **Signature whistles:** Unique individual identifiers (like "names")
  - **Pulsed calls:** Complex harmonics for social contexts
- Function: Social communication, individual recognition, group coordination
- Memory: Dolphins remember signature whistles for 20+ years
- Our EARS data: **Perfectly suited** - 192 kHz easily captures 2-20 kHz range

**Key Insights:**

- Acoustic processing brain area is 10x larger than human
- Dolphins understand complex syntax and word order
- Vocal learning capability (rare in mammals)
- Species-specific dialects exist
- Self-awareness and theory of mind demonstrated

## Available Data

- **Location:** `data/Buoy210_100300_100399/`
- **Count:** 100 files (\*.210 format)
- **Format:** EARS - 16-bit signed integers, big-endian
- **Sampling Rate:** 192,000 Hz (192 kHz)
- **Recording:** Gulf of Mexico underwater acoustic monitoring
- **Suitability:**
  - ✅ Excellent for whistles (2-20 kHz)
  - ⚠️ Limited for highest frequency clicks (96 kHz max vs 220+ kHz optimal)
  - ✅ Good for mid-frequency clicks (up to 96 kHz)

## Existing Codebase Structure

```
dolphain/
├── __init__.py          # Fixed with __version__ = "0.1.0"
├── io.py                # EARS file reading
├── signal.py            # Wavelet denoising
├── plotting.py          # Visualization tools
└── batch.py             # NEW - Batch processing framework

examples/
├── ears_analysis_demo.ipynb       # Basic usage
├── wavelet_demo.ipynb             # Denoising tutorial
└── batch_experiments.ipynb        # Batch framework demo

docs/
├── BATCH_PROCESSING.md            # User guide
├── BATCH_IMPLEMENTATION.md        # Technical details
├── DEVELOPMENT_INSTALL.md         # Installation guide
└── NEXT_STEPS.md                  # Action plan
```

## NEXT IMMEDIATE TASK 🎯

### Create: `examples/dolphin_communication_analysis.ipynb`

This is the **primary research notebook** - everything built so far supports this analysis.

### Notebook Structure (7 Sections)

#### 1. Introduction & Background

- Overview of dolphin communication research
- Acoustic characteristics of clicks vs whistles
- Research objectives for this analysis
- EARS data specifications and limitations
- Scientific context and citations

#### 2. Signal Detection Module

**Goal:** Identify dolphin vocalizations in recordings

**Clicks Detection (High-Frequency):**

```python
# Frequency range: 20-96 kHz (limited by Nyquist)
# Method: High-pass filter + energy detector
# Threshold: Adaptive based on background noise
# Output: Click times, inter-click intervals (ICI)
```

**Whistle Extraction (Mid-Frequency):**

```python
# Frequency range: 2-20 kHz
# Method: Band-pass filter + spectrogram analysis
# Technique: Contour following algorithm
# Output: Whistle start/end times, frequency contours
```

**Implementation Approach:**

- Spectrogram analysis (STFT with appropriate window)
- Adaptive thresholding for noise robustness
- Peak detection in frequency domain
- Temporal clustering for call sequences

#### 3. Feature Extraction

**Click Features:**

- Inter-click intervals (ICI) - typical patterns vs hunting buzz
- Click duration and amplitude
- Peak frequency (if within 96 kHz range)
- Click train characteristics

**Whistle Features:**

- Duration measurements
- Frequency range (min/max)
- Frequency modulation patterns (FM contours)
- Harmonic structure
- Contour shape descriptors (for signature identification)

**Output:** Feature DataFrame for statistical analysis

#### 4. Classification Algorithms

**Vocalization Type Classification:**

- Click vs whistle discrimination (straightforward - frequency separation)
- Click subtypes: Regular echolocation vs terminal buzz vs social clicks
- Whistle subtypes: Signature vs non-signature patterns

**Methods to Implement:**

- Threshold-based classification (frequency, duration, ICI)
- Clustering analysis (K-means, DBSCAN) for signature whistle grouping
- Template matching for known signature whistle patterns
- Statistical feature analysis

**Signature Whistle Detection:**

- Contour extraction and comparison
- Dynamic Time Warping (DTW) for pattern matching
- Build signature catalog from repeated patterns

#### 5. Batch Analysis Framework

**Goal:** Process multiple files systematically

```python
from dolphain.batch import BatchProcessor, BatchExperiment

# Define detection pipeline
def detect_dolphins(file_path):
    data, sr = read_ears_file(file_path)
    clicks = detect_clicks(data, sr)
    whistles = detect_whistles(data, sr)
    return {
        'clicks': clicks,
        'whistles': whistles,
        'click_count': len(clicks),
        'whistle_count': len(whistles)
    }

# Process all files
processor = BatchProcessor()
results = processor.process_files(file_list, detect_dolphins)
```

**Outputs:**

- Detection statistics per file
- Temporal distribution (when dolphins are present)
- Aggregated feature distributions
- Signature whistle catalog across files

#### 6. Visualization Suite

**Essential Plots:**

1. **Spectrogram with Overlays:**

   - Raw spectrogram (0-96 kHz)
   - Detected clicks marked
   - Whistle contours overlaid
   - Color-coded by classification

2. **Whistle Contour Gallery:**

   - Individual whistle frequency vs time
   - Grouped by similarity (potential signatures)
   - Comparison plots for signature matching

3. **Click Analysis:**

   - Inter-click interval histogram
   - Click train timing diagrams
   - Amplitude distribution

4. **Temporal Distribution:**

   - Vocalization events over time
   - Click rate vs whistle rate
   - Activity patterns (if time metadata available)

5. **Feature Space Visualization:**

   - PCA/t-SNE of whistle features
   - Clustering visualization
   - Signature whistle grouping

6. **Batch Results Dashboard:**
   - Detection rate across files
   - Feature distributions
   - Statistical summaries

#### 7. Language Analysis & Interpretation

**Advanced Analysis:**

1. **Sequence Pattern Detection:**

   - Call type sequences (click-whistle patterns)
   - Temporal associations
   - Context-dependent usage

2. **Signature Whistle Catalog:**

   - Unique signature identification
   - Individual tracking across recordings
   - Social network analysis (if multiple individuals)

3. **Communication Event Classification:**

   - Echolocation events (hunting, navigation)
   - Social communication events
   - Contact calls vs signature whistles

4. **Statistical Analysis:**
   - Call rate statistics
   - Feature correlations
   - Temporal patterns

**Interpretation Guidelines:**

- Compare findings to published dolphin acoustic literature
- Note limitations (96 kHz ceiling, single hydrophone)
- Suggest future work (higher sampling rate, stereophonic recording)

## Technical Implementation Notes

### Critical Parameters

**STFT Settings for Spectrogram:**

```python
# For clicks (high frequency):
nperseg = 256      # Short window for time resolution
noverlap = 128     # 50% overlap
fmax = 96000       # Nyquist limit

# For whistles (mid frequency):
nperseg = 2048     # Longer window for frequency resolution
noverlap = 1536    # 75% overlap
fmin = 2000, fmax = 20000  # Whistle band
```

**Detection Thresholds:**

- Start with conservative (high specificity)
- Implement adaptive thresholding based on noise floor
- Validate against known dolphin acoustic parameters

**Performance Optimization:**

- Process files in chunks for large datasets
- Use batch framework for parallel processing potential
- Cache intermediate results (spectrograms)

### Key Algorithms to Implement

1. **Click Detection:**

   - High-pass filter (>20 kHz)
   - Teager-Kaiser energy operator
   - Peak detection with minimum spacing
   - ICI calculation

2. **Whistle Contour Extraction:**

   - Spectrogram peak tracking
   - Ridge following algorithm
   - Minimum duration filter (>0.1s)
   - Maximum gap bridging

3. **Signature Whistle Matching:**
   - Dynamic Time Warping (DTW) distance
   - Cross-correlation of contours
   - Clustering coefficient for grouping

## Scientific Context & References

**Key Marine Mammal Bioacoustics Concepts:**

- Dolphins use biosonar for navigation (active sensing)
- Signature whistles are individually specific and learned
- Click rates indicate behavioral state (search vs capture)
- Frequency modulation patterns carry information
- Social context affects vocalization rates

**Recommended Citations to Include:**

- Tyack & Clark on signature whistles
- Au on dolphin sonar capabilities
- Janik on vocal learning in dolphins
- EARS system technical specifications

## Code Snippets to Include

### File Reading Template

```python
import dolphain
from dolphain.io import read_ears_file
import numpy as np

# Read EARS file
file_path = '../data/Buoy210_100300_100399/Buoy210.100300'
data, sample_rate = read_ears_file(file_path)
print(f"Duration: {len(data)/sample_rate:.1f} seconds")
print(f"Sample rate: {sample_rate} Hz")
```

### Basic Spectrogram

```python
from scipy import signal
import matplotlib.pyplot as plt

# Compute spectrogram
f, t, Sxx = signal.spectrogram(
    data,
    fs=sample_rate,
    nperseg=2048,
    noverlap=1536
)

# Plot (focus on dolphin range)
plt.figure(figsize=(15, 6))
plt.pcolormesh(t, f/1000, 10*np.log10(Sxx), shading='gouraud')
plt.ylim([0, 50])  # 0-50 kHz
plt.ylabel('Frequency (kHz)')
plt.xlabel('Time (s)')
plt.colorbar(label='Power (dB)')
plt.title('Spectrogram - Dolphin Frequency Range')
```

### Click Detection Skeleton

```python
def detect_clicks(data, sr, threshold_db=-40):
    """Detect potential dolphin clicks in high-frequency range."""
    from scipy.signal import butter, filtfilt

    # High-pass filter (>20 kHz)
    nyq = sr / 2
    fc = 20000  # 20 kHz cutoff
    b, a = butter(4, fc/nyq, 'high')
    filtered = filtfilt(b, a, data)

    # Energy detection
    energy = filtered ** 2
    # ... threshold detection logic

    return click_times, click_features
```

### Whistle Detection Skeleton

```python
def detect_whistles(data, sr, min_duration=0.1):
    """Extract dolphin whistle contours from spectrogram."""
    # Band-pass filter (2-20 kHz)
    from scipy.signal import butter, filtfilt

    nyq = sr / 2
    low = 2000 / nyq
    high = 20000 / nyq
    b, a = butter(4, [low, high], 'band')
    filtered = filtfilt(b, a, data)

    # Spectrogram with good frequency resolution
    f, t, Sxx = signal.spectrogram(filtered, sr, nperseg=2048, noverlap=1536)

    # Ridge detection / contour following
    # ... tracking logic

    return whistle_contours, whistle_features
```

## Commands Ready to Execute

When starting new session:

```bash
# Navigate to project
cd /Users/mjhaas/code/dolphain

# Activate environment (if needed)
source .venv/bin/activate

# Verify installation
python -c "import dolphain; print(dolphain.__version__)"

# List available data
ls -lh data/Buoy210_100300_100399/ | head -10

# Launch Jupyter
jupyter notebook examples/
```

## Session Restart Instructions

1. **Read this file first:** `SESSION_STATE.md`
2. **Context:** All infrastructure is complete; create the dolphin analysis notebook
3. **Next Action:** Create `examples/dolphin_communication_analysis.ipynb`
4. **Approach:**
   - Start with Section 1 (Introduction)
   - Implement detection algorithms (Sections 2-3)
   - Add visualization (Section 6)
   - Build up to full analysis (Sections 4-5-7)
5. **Reference:** Use code snippets and parameters from this document
6. **Validate:** Test each section with actual EARS data as you build

## Important Reminders

- **192 kHz sampling** means we can analyze up to **96 kHz** (Nyquist limit)
- This covers **all dolphin whistles** (2-20 kHz) perfectly
- This covers **mid-range clicks** but misses highest frequency components (>96 kHz)
- Focus on **signature whistles** as they're the "language" component
- Click **inter-click intervals** (ICI) reveal behavioral state
- The batch framework is ready for processing all 100 files once detection works

## Research Question

**"Can we detect, classify, and understand dolphin communication patterns in Gulf of Mexico EARS recordings?"**

The answer requires:

1. ✅ Infrastructure (batch processing) - DONE
2. ✅ Scientific knowledge (dolphin acoustics) - ACQUIRED
3. 🔄 Detection algorithms - TO BUILD
4. 🔄 Analysis notebook - TO CREATE
5. 🔄 Results & interpretation - FUTURE

## Status: READY TO BUILD NOTEBOOK

All prerequisites complete. Create the notebook and start detecting dolphins! 🐬
