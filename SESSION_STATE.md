# Dolphain Project - Session State & Continuation Guide

**Last Updated:** October 10, 2025  
**Status:** Dolphin communication notebook in progress (click detection prototype running on small chunks)

## Current Location & Context

- **Working Directory:** `/Users/mjhaas/code/dolphain`
- **Active File:** `examples/dolphin_communication_analysis.ipynb` (click detection section)
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

## ACTIVE ROADMAP 🎯

### Notebook Milestones (macro view)

1. ✅ **Click detection prototype** (5 s chunk, Teager-Kaiser energy)
2. ⏳ **Click post-processing** (filter false positives, cluster into trains)
3. ⏳ **Whistle detection module** (band-pass + contour tracking)
4. ⏳ **Feature extraction + summaries**
5. ⏳ **Batch processing integration**
6. ⏳ **Visualization + interpretation write-up**

### Focus for the Next Session (bite-sized)

1. **Review click detection outputs**

   - Inspect amplitude & ICI distributions for realism
   - Plot raw waveform snippets around sample clicks
   - Adjust `threshold_factor` / smoothing window as needed

2. **Add safety rails before scaling up**

   - Wrap detection in helper that enforces `max_chunk_duration`
   - Add runtime guard (`max_runtime_s`) with early exit + log
   - Prepare generator to iterate over chunks lazily (`yield from chunk_signal`)

3. **Prepare whistle detection scaffold**

   - Draft function signature & docstring
   - Outline band-pass filtering and spectrogram params without executing heavy loops yet

4. **Document decisions in notebook markdown**
   - Note current parameter choices & rationale
   - Record guard-rail strategy to prevent runaway cells

### Guard Rails & Context Hygiene 🧭

- When running heavy analysis cells, **always operate on ≤5 s chunks** unless explicitly timed.
- Use `with Timer(max_seconds=30)` (to be implemented) or manual `time.perf_counter()` checks to abort long loops.
- Keep notebook sections modular: execute/inspect one block at a time; restart kernel before multi-minute runs.
- After each session, update this file and trim notebook outputs (especially large arrays) to keep the context light.

### Quick TODO Snapshot (persisted)

- [ ] Validate high-count buoy recordings with waveform + spectrogram overlays (focus on retention beyond threshold 6).
- [ ] Extend chunk scanning using `iterate_chunks` (≥3 additional windows per representative file) and store results in `reports/`.
- [ ] Draft whistle detection scaffold (function signature, band-pass filter, placeholder for contour extraction).
- [ ] Update README “Examples” section to mention dolphin communication notebook and `reports/` outputs.

### Fresh TODOs After 2025-10-10 Session

- [ ] Investigate high click counts (11,953 in 5 s) — confirm they're broadband impulses vs noise; consider stricter smoothing window or adaptive thresholding tweaks.
- [ ] Extend sanity check to additional chunks (use `iterate_chunks`) and log summary stats per chunk to `reports/`.
- [x] Compare click metrics after threshold sweep (4/6/8) for buoy vs special files and note parameter sensitivity.

### Latest Results (2025-10-10)

- Sampled **10 buoy** files (seed 42) and **2 special** files (`71621DC7 (1).190`, `7164403B.130`) using the first 5 seconds per recording.
- Buoy chunks averaged **2325 clicks** (465 clicks/s) with median ICI ≈ 0.148 ms; special chunks averaged **446 clicks** (89 clicks/s) with median ICI ≈ 0.219 ms.
- Threshold sweep revealed buoy detections retain ~37% of baseline at threshold 6 and ~22% at threshold 8, while special files drop to <5% and ~1%, respectively.
- Saved detailed metrics to `reports/click_comparison_buoy_vs_special.csv`, threshold sweep details to `reports/click_threshold_sweep_details.csv`, and summary aggregates to `reports/click_threshold_sweep_summary.csv`.
- New visual summaries: “Mean Click Rate vs Threshold” and “Detection Retention by File” illustrate likely false positives (steep drop-offs) versus resilient detections.

### Latest Results (2025-10-10)

- Sampled **10 buoy** files (seed 42) and **2 special** files (`71621DC7 (1).190`, `7164403B.130`) using the first 5 seconds per recording.
- Buoy chunks averaged **2325 clicks** (465 clicks/s) with median ICI ≈ 0.148 ms; special chunks averaged **446 clicks** (89 clicks/s) with median ICI ≈ 0.219 ms.
- Threshold sweep revealed buoy detections retain ~37% of baseline at threshold 6 and ~22% at threshold 8, while special files drop to <5% and ~1%, respectively.
- Saved detailed metrics to `reports/click_comparison_buoy_vs_special.csv`, with sweep details in `reports/click_threshold_sweep_details.csv` and summary aggregates in `reports/click_threshold_sweep_summary.csv`.
- New plots (“Mean Click Rate vs Threshold”, “Detection Retention by File”) offer a quick look at probable false positives.
- No runtime issues: each file processed <0.25 s with guardrails engaged.

> ✅ Update this checklist as items are completed. Keep each box scoped to a <30 minute effort to avoid runaway work sessions.

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
