# Dolphain Project - Continuation Guide

**Date:** October 10, 2025  
**Purpose:** Complete guide for resuming work on this project after any break  
**Status:** Click detection prototyped in notebook; ready for whistle detection

---

## 🎯 Project Mission

**Analyze underwater acoustic recordings (EARS data) to detect, classify, and understand dolphin communication through clicks and whistles.**

This is marine biology research - we're trying to understand dolphin "language" from real-world recordings in the Gulf of Mexico.

---

## 📂 Quick Orientation

### What You're Working With

- **Location:** `/Users/mjhaas/code/dolphain`
- **Data:** 100 EARS files in `data/Buoy210_100300_100399/` (*.210 format, 192 kHz sampling)
- **Python Env:** `.venv` (already installed with `pip install -e .`)
- **Active Notebook:** `examples/dolphin_communication_analysis.ipynb`
- **Git:** Repository is `micha2718l/dolphain` on GitHub (branch: main)

### Project Structure

```
dolphain/
├── dolphain/                     # Core library (STABLE & TESTED)
│   ├── __init__.py              # Package with __version__
│   ├── io.py                    # EARS file reading
│   ├── signal.py                # Wavelet denoising
│   ├── plotting.py              # Visualization
│   └── batch.py                 # Batch processing framework
├── examples/                     # Research notebooks
│   ├── dolphin_communication_analysis.ipynb  # ACTIVE WORK HERE
│   ├── batch_experiments.ipynb
│   └── ears_analysis_demo.ipynb
├── data/                        # Acoustic recordings
│   ├── Buoy210_100300_100399/  # 100 buoy recordings
│   └── special/                 # 2 comparison files
├── tests/                       # Unit tests (passing)
├── docs/                        # Documentation
└── [various .md files]          # Project state docs
```

---

## ✅ What's Already Complete

### 1. Core Library (100% Done - Don't Touch)
- ✅ File I/O for EARS formats (.130, .190, .210)
- ✅ Wavelet denoising (VisuShrink algorithm)
- ✅ Plotting utilities (waveforms, spectrograms)
- ✅ Batch processing framework
- ✅ All tests passing
- ✅ Package installed and importable

**Documentation:** See `BATCH_PROCESSING.md`, `BATCH_IMPLEMENTATION.md`, `README.md`

### 2. Research Foundation (Done)
- ✅ Dolphin acoustics research (from Wikipedia)
  - **Clicks:** >110 kHz, echolocation, brief pulses
  - **Whistles:** 2-20 kHz, communication, 0.5-1.5 sec duration
  - **Signature whistles:** Individual "names" dolphins remember for 20+ years
- ✅ Data assessment: 192 kHz sampling is perfect for whistles, good for mid-range clicks
- ✅ Scientific context documented in `SESSION_STATE.md` (lines 70-107)

### 3. Active Notebook Progress
- ✅ Setup and imports
- ✅ Click detection prototype (Teager-Kaiser energy operator)
- ✅ Basic testing on small chunks (5 seconds)
- ✅ Runtime guardrails implemented (prevent runaway cells)
- ⏳ Whistle detection (not started)
- ⏳ Full dataset batch processing (not started)

**Note:** The notebook mentions saving to `reports/` directory but this wasn't actually created. Outputs exist only in notebook variables.

---

## 🚀 How to Resume Work

### Step 1: Get Your Bearings (5 minutes)

```bash
# Navigate to project
cd /Users/mjhaas/code/dolphain

# Check git status
git status

# Activate Python environment (if not already active)
source .venv/bin/activate

# Verify installation
python -c "import dolphain; print(f'Version: {dolphain.__version__}')"

# Open the active notebook
jupyter notebook examples/dolphin_communication_analysis.ipynb
```

### Step 2: Review Current State (10 minutes)

1. Read the notebook from top to bottom (don't execute yet)
2. Note which cells have been executed (look for execution counts)
3. Check notebook variables - there are many computed results already in memory
4. Key variables to inspect:
   - `click_times`, `click_amps`, `ici_ms` - click detection results
   - `comparison_df` - buoy vs special file comparison
   - `threshold_df` - threshold sweep results

### Step 3: Decide Your Path

Choose based on your goal:

**Path A: Continue Where You Left Off (Whistle Detection)**
- Jump to "Next Steps: Whistle Detection" section below
- Estimated time: 2-4 hours for initial implementation

**Path B: Review and Persist Existing Work**
- Create `reports/` directory
- Re-run cells that generate comparison/sweep data
- Save CSVs and plots to disk
- Estimated time: 30-60 minutes

**Path C: Start Fresh with Clean Slate**
- Restart notebook kernel
- Execute cells one by one from top
- Verify all results reproduce
- Estimated time: 1-2 hours

---

## 🎯 Next Steps: Whistle Detection

### The Goal
Detect and extract dolphin whistle contours (2-20 kHz, 0.5-1.5 sec duration).

### Implementation Plan (Chunked for Context Management)

#### Chunk 1: Setup (15 minutes)
```python
# Add to notebook - Section 2.2: Whistle Detection

from scipy.signal import butter, filtfilt, spectrogram
import numpy as np
import pandas as pd

def detect_whistles(signal_array, fs, 
                   band=(2000, 20000), 
                   min_duration=0.1,
                   threshold_factor=3.0):
    """
    Detect dolphin whistles in frequency band 2-20 kHz.
    
    Parameters:
    -----------
    signal_array : ndarray
        Audio signal
    fs : int
        Sample rate (Hz)
    band : tuple
        (low_freq, high_freq) in Hz
    min_duration : float
        Minimum whistle duration (seconds)
    threshold_factor : float
        Threshold as multiple of median energy
    
    Returns:
    --------
    whistles : list of dict
        Each dict contains: start_time, end_time, freq_contour, etc.
    """
    # TODO: Implement
    raise NotImplementedError("Start here!")
```

#### Chunk 2: Band-pass Filter (20 minutes)
```python
# Inside detect_whistles function:

# 1. Band-pass filter
nyq = fs / 2
low = band[0] / nyq
high = band[1] / nyq
b, a = butter(4, [low, high], btype='band')
filtered = filtfilt(b, a, signal_array)

print(f"Filtered to {band[0]/1000}-{band[1]/1000} kHz range")
```

**Test it:** Apply to 5-second chunk, plot filtered vs original waveform.

#### Chunk 3: High-Res Spectrogram (30 minutes)
```python
# 2. Generate spectrogram with good frequency resolution
nperseg = 2048      # Longer window for better freq resolution
noverlap = 1536     # 75% overlap for smooth contours

f, t, Sxx = spectrogram(filtered, fs, 
                        nperseg=nperseg, 
                        noverlap=noverlap)

# Convert to dB
Sxx_db = 10 * np.log10(Sxx + 1e-10)

print(f"Spectrogram shape: {Sxx.shape}")
print(f"Time resolution: {t[1]-t[0]:.4f} s")
print(f"Freq resolution: {f[1]-f[0]:.1f} Hz")
```

**Test it:** Plot spectrogram, verify you can see potential whistles visually.

#### Chunk 4: Ridge Detection (1-2 hours)
```python
# 3. Extract spectral ridges (simplified approach)
# For each time bin, find the frequency bin with peak energy
# that's above threshold

threshold = np.median(Sxx_db) + threshold_factor

contours = []
for t_idx in range(Sxx.shape[1]):
    spectrum = Sxx_db[:, t_idx]
    peak_idx = np.argmax(spectrum)
    peak_value = spectrum[peak_idx]
    
    if peak_value > threshold:
        contours.append({
            'time': t[t_idx],
            'freq': f[peak_idx],
            'power': peak_value
        })

# Convert to DataFrame for easier manipulation
contour_df = pd.DataFrame(contours)
```

**Test it:** Plot detected points over spectrogram, verify they follow visible whistles.

#### Chunk 5: Contour Grouping (1 hour)
```python
# 4. Group consecutive points into whistle events
# Points within 0.1s and 500 Hz are considered same whistle

whistles = []
if len(contour_df) > 0:
    # Group by time proximity
    contour_df['time_diff'] = contour_df['time'].diff()
    contour_df['new_whistle'] = contour_df['time_diff'] > 0.1
    contour_df['whistle_id'] = contour_df['new_whistle'].cumsum()
    
    # Process each whistle
    for wid in contour_df['whistle_id'].unique():
        w = contour_df[contour_df['whistle_id'] == wid]
        duration = w['time'].max() - w['time'].min()
        
        if duration >= min_duration:
            whistles.append({
                'start_time': w['time'].min(),
                'end_time': w['time'].max(),
                'duration': duration,
                'freq_min': w['freq'].min(),
                'freq_max': w['freq'].max(),
                'freq_mean': w['freq'].mean(),
                'num_points': len(w)
            })

print(f"Found {len(whistles)} whistles")
```

**Test it:** Verify durations make sense (0.1-3 seconds typical).

---

## 🛡️ Critical Best Practices (MUST FOLLOW)

### 1. Chunk Processing (Prevent Runaway Memory/Time)

**ALWAYS** work with small chunks first:

```python
# Good: Start with 5 seconds
chunk_duration = 5.0
chunk_samples = int(chunk_duration * sample_rate)
test_chunk = data[:chunk_samples]

# Bad: Don't process entire file until tested
# full_result = analyze_entire_file(data)  # ❌ Could take forever
```

### 2. Timing Guards

**ALWAYS** time expensive operations:

```python
import time

start = time.perf_counter()
# ... expensive operation ...
elapsed = time.perf_counter() - start
print(f"Completed in {elapsed:.2f} seconds")

# Set maximum runtime guards
MAX_RUNTIME = 30  # seconds
if elapsed > MAX_RUNTIME:
    print(f"⚠️ Operation exceeded {MAX_RUNTIME}s limit")
```

### 3. Incremental Persistence

**SAVE RESULTS FREQUENTLY** to avoid losing work:

```python
# After each major analysis step:
import pandas as pd
from pathlib import Path

# Create reports directory if needed
reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)

# Save results
results_df.to_csv(reports_dir / "whistle_detection_results.csv", index=False)
print(f"Saved results to {reports_dir}")

# Save plots
import matplotlib.pyplot as plt
fig.savefig(reports_dir / "whistle_contours.png", dpi=150, bbox_inches='tight')
plt.close(fig)
print("Saved figure")
```

### 4. Progress Tracking

For batch operations over many files:

```python
# Use tqdm or manual progress
from tqdm import tqdm

results = []
for i, file_path in enumerate(tqdm(file_list[:10])):  # Start with 10 files
    # Process file
    result = process_file(file_path)
    results.append(result)
    
    # Save checkpoint every 5 files
    if (i + 1) % 5 == 0:
        pd.DataFrame(results).to_csv(f"checkpoint_{i+1}.csv")
```

### 5. Context Window Management

Keep this guide open and refer to it. Update it as you learn:

```python
# At end of each work session, add notes:
# - What worked well
# - What parameters to try next
# - Any gotchas discovered
# - Next 3 concrete steps
```

---

## 📊 Parameter Reference

### Click Detection (Already Implemented)
```python
# In notebook - Section 2.1
threshold_factor = 4.0      # Start conservative
smoothing_window = 51       # Smooth Teager-Kaiser energy
min_spacing = 0.0001        # 0.1 ms minimum between clicks
```

### Whistle Detection (To Implement)
```python
# Recommended starting values
band = (2000, 20000)        # Hz - dolphin whistle range
min_duration = 0.1          # seconds
threshold_factor = 3.0      # above median spectrogram energy
nperseg = 2048             # ~10 ms time resolution at 192 kHz
noverlap = 1536            # 75% overlap
```

### Spectrogram Settings
```python
# For clicks (high freq, good time resolution)
nperseg = 256
noverlap = 128
fmax = 96000  # Nyquist limit

# For whistles (mid freq, good freq resolution)
nperseg = 2048
noverlap = 1536
fmin = 2000
fmax = 20000
```

---

## 🔄 Session Workflow

### Start of Session (10 minutes)
1. ✅ Read this guide (or `SESSION_STATE.md` for detailed state)
2. ✅ Check git status: `git status`
3. ✅ Review what changed since last session
4. ✅ Activate environment: `source .venv/bin/activate`
5. ✅ Open notebook: `jupyter notebook examples/dolphin_communication_analysis.ipynb`
6. ✅ Decide on 1-2 hour goal for this session

### During Session
- ⏰ Set a timer for your planned work duration
- 💾 Save results every 30 minutes
- 📝 Add markdown cells explaining what you're doing
- 🧪 Test each function on small data before scaling up
- 📊 Create visualizations to validate results

### End of Session (15 minutes)
1. 💾 Save all notebooks
2. 📁 Ensure any new data/plots saved to `reports/`
3. 📝 Update `SESSION_STATE.md` with:
   - What was accomplished
   - Any new findings
   - Specific next steps (be concrete!)
   - Any gotchas or issues encountered
4. 🗑️ Clear large notebook outputs if needed (kernel → restart & clear)
5. 💾 Commit and push:
   ```bash
   git add -A
   git commit -m "Session YYYY-MM-DD: Brief description of work"
   git push origin main
   ```

---

## 📚 Documentation Map

Know where to look for what:

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `CONTINUATION_GUIDE.md` (this file) | How to resume work | START OF EVERY SESSION |
| `SESSION_STATE.md` | Detailed current state | For deeper context on research |
| `PROJECT_STATUS.md` | High-level project status | To understand overall progress |
| `NEXT_STEPS.md` | Prioritized action items | When choosing what to work on |
| `README.md` | Core library usage | When using library functions |
| `BATCH_PROCESSING.md` | Batch framework guide | When processing many files |
| `BATCH_IMPLEMENTATION.md` | Technical implementation | When modifying batch system |

---

## 🎓 Lessons Learned (Update as You Go)

### What Works Well
- ✅ Starting with 5-second chunks prevents runaway processing
- ✅ Teager-Kaiser energy operator is effective for click detection
- ✅ Threshold sweep (4/6/8) helps assess parameter sensitivity
- ✅ Comparison between buoy and special files reveals false positive rates

### Gotchas
- ⚠️ Don't reference `reports/` directory until it's actually created
- ⚠️ Notebook variables persist between sessions (restart kernel for clean slate)
- ⚠️ Large spectrograms can consume lots of memory (work in chunks)
- ⚠️ EARS files are big-endian, 16-bit signed integers (library handles this)

### Parameters That Need Tuning
- 🎚️ Click threshold_factor: 4 catches many, 6-8 more conservative
- 🎚️ Whistle min_duration: 0.1s is lower bound, most are 0.5-1.5s
- 🎚️ Smoothing window: 51 samples works, may need adaptation per file

---

## 🚨 If You Get Stuck

### Context Window Getting Full?
1. Restart this conversation
2. Say: "Read CONTINUATION_GUIDE.md and help me continue"
3. Provide specific question/goal

### Notebook Kernel Issues?
```bash
# Restart kernel and re-run from top
# Or start fresh
jupyter notebook --no-browser
# Then open browser manually
```

### Git Conflicts?
```bash
git status
git stash  # Save your changes
git pull origin main
git stash pop  # Reapply your changes
# Resolve any conflicts, then commit
```

### Environment Issues?
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 📈 Success Metrics

You'll know you're making progress when:

- ✅ Whistle detection function runs without errors on test chunk
- ✅ Visual inspection shows detected contours match visible whistles
- ✅ Detection statistics (count, duration, frequency) are scientifically reasonable
- ✅ Function works on multiple different files
- ✅ Results are saved to disk and reproducible
- ✅ Documentation is updated with findings

---

## 🎯 Big Picture Goals

**Short-term (Next 1-2 Sessions):**
- [ ] Implement whistle detection function
- [ ] Test on 5-10 files
- [ ] Create visualizations of detected whistles
- [ ] Save results to `reports/` directory

**Medium-term (Next 5-10 Sessions):**
- [ ] Refine detection parameters based on validation
- [ ] Process full dataset (100 files) using batch framework
- [ ] Build summary statistics and visualizations
- [ ] Identify files with high whistle activity

**Long-term (Future):**
- [ ] Implement signature whistle matching
- [ ] Classify whistle types
- [ ] Temporal analysis (when do dolphins communicate?)
- [ ] Publish findings or create interactive visualization

---

## 🐬 Remember

You're not just writing code - you're helping understand how dolphins communicate! 

Every detected whistle is potentially a dolphin "name" or social signal. The patterns you find could reveal:
- Individual identification
- Social group structure  
- Behavioral patterns
- Communication complexity

Stay curious, be methodical, and document your discoveries!

---

**Last Updated:** October 10, 2025  
**Next Review:** Update this file at end of each session with new learnings
