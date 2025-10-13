# 🔬 Conservative Click Train Detection Experiment

**Date:** October 12, 2025  
**Purpose:** Test more conservative click train detection on 1000 random files

---

## 🎯 Modifications Made

### Changes to `detect_click_trains()` in `scripts/quick_find.py`

#### 1. **Higher Thresholds**
- **Percentile:** 99th → **99.5th** percentile
- **Noise ratio:** 8x → **10x** noise level
- *Result:* Only detects the very strongest clicks

#### 2. **Sharper Peak Requirements**
- **Prominence:** 30% → **40%** of threshold
- **Width constraint:** 1-5ms → **1-3ms** (tighter for sharper peaks)
- **Local dominance:** 90th → **92nd** percentile within 4ms window
- *Result:* Rejects wider bumps, accepts only sharp spikes

#### 3. **More Clicks Required**
- **Minimum clicks per train:** 10 → **15**
- *Result:* Only detects longer, more sustained trains

#### 4. **Regularity Check (NEW)**
- **Coefficient of Variation (CV):** Must be < 0.5
  - CV = std_ici / mean_ici
  - CV < 0.5 means ICI std is less than 50% of mean
- *Result:* Only accepts trains with consistent click spacing (real spike trains)
- **New field added:** `regularity_cv` in results for analysis

---

## 🔍 Expected Outcomes

### Before (Original Algorithm)
- Min clicks: 10
- Threshold: 99th percentile, 8x noise
- Width: up to 5ms
- No regularity check
- **Expected:** More detections, some false positives

### After (Conservative Algorithm)
- Min clicks: 15
- Threshold: 99.5th percentile, 10x noise  
- Width: up to 3ms (tighter)
- Regularity: CV < 0.5 required
- **Expected:** Fewer detections, higher precision, more genuine spike trains

---

## 📊 Test Command

Run this in a **separate terminal** (not the one running your LLM session):

```bash
cd /Users/mjhaas/code/dolphain

# Activate virtual environment if needed
source .venv/bin/activate

# Run analysis on 1000 random files
python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --output-dir quick_find_results/conservative_clicks_experiment
```

---

## 📁 Output Structure

Results will be saved to: `quick_find_results/conservative_clicks_experiment/`

Files generated:
- **`results.json`** - Full results with all detections
- **`summary.json`** - Statistics summary
- **`all_results.csv`** - Spreadsheet format
- **`top_20_files.txt`** - List of most interesting files
- **`checkpoint.json`** - Resume point (if interrupted)

---

## 🔬 Analysis Questions

After running, compare with previous results to answer:

1. **Detection Rate:**
   - How many files had click trains detected?
   - How does this compare to previous runs?

2. **Click Train Quality:**
   - What's the average `regularity_cv` value?
   - Are trains longer (more clicks per train)?

3. **False Positive Rate:**
   - Do the top-scoring files look more convincing?
   - Are there fewer noise-triggered detections?

4. **Interestingness Scores:**
   - How do scores compare to previous runs?
   - Are high-scoring files more concentrated (fewer spread across mid-range)?

---

## 📈 Next Steps

Based on results:

### If Too Conservative (very few detections)
- Reduce `regularity_cv` threshold from 0.5 to 0.6 or 0.7
- Lower percentile from 99.5 back to 99.2
- Reduce min_clicks from 15 to 12

### If Still Too Permissive (noise/false positives)
- Increase `regularity_cv` threshold even more (0.4 or 0.3)
- Add frequency domain check (clicks should be broadband)
- Require minimum train duration

### If Just Right
- Document the parameters
- Run on larger sample (5000-10000 files)
- Generate showcase with best examples

---

## 💾 Reverting Changes

If you want to revert to original algorithm:

```bash
git diff scripts/quick_find.py  # See changes
git checkout scripts/quick_find.py  # Revert to original
```

Or manually change back:
- `min_clicks=15` → `min_clicks=10`
- `99.5` → `99`
- `10` → `8` (noise multiplier)
- `0.4` → `0.3` (prominence)
- `0.003` → `0.005` (width)
- `92` → `90` (percentile)
- Remove `cv < 0.5` check (lines ~298-333)

---

## 📝 Key Algorithm Changes Summary

```python
# OLD:
min_clicks=10
threshold = np.percentile(envelope, 99)
min_click_amplitude = noise_level * 8
prominence=threshold * 0.3
width=(1, int(fs * 0.005))
if peak_val > np.percentile(local_region, 90):
    sharp_peaks.append(idx)
# (no regularity check)

# NEW:
min_clicks=15
threshold = np.percentile(envelope, 99.5)
min_click_amplitude = noise_level * 10
prominence=threshold * 0.4
width=(1, int(fs * 0.003))
if peak_val > np.percentile(local_region, 92):
    sharp_peaks.append(idx)
# Added regularity check:
cv = std_ici / mean_ici
if cv < 0.5:  # Only accept regular trains
    click_trains.append(...)
```

---

## 🎓 Technical Notes

### What is Coefficient of Variation (CV)?

CV = std / mean

- **CV = 0.2:** Very regular (20% variation)
- **CV = 0.5:** Moderately regular (50% variation) ← our threshold
- **CV = 1.0:** Highly variable (100% variation)
- **CV > 1.0:** Standard deviation exceeds mean (very irregular)

### Real Dolphin Click Trains

From literature:
- **ICI (Inter-Click Interval):** 5-100ms, typically 20-50ms
- **Regularity:** Usually quite regular (CV < 0.4 for echolocation)
- **Duration:** Trains often 0.5-3 seconds
- **Click count:** 10-60+ clicks per train
- **Peak width:** Very narrow, <1ms for many species

Our conservative settings target the clearest examples.

---

**Ready to run!** The algorithm is now more conservative. Test it and see how the results compare! 🚀
