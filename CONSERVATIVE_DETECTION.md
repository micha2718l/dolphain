# Conservative Detection Update

## Overview
Updated the chirp and click train detection algorithms to be MUCH more selective, per user feedback that "detection algorithms are way too aggressive."

## Changes Made

### 1. Chirp Detection (`detect_chirps`)
**Goal**: Only detect strong, clear frequency sweeps across time, not noise variations

**Parameter Updates**:
- `nperseg`: 4096 → **8192** (better frequency resolution, slower sweep tracking)
- `threshold`: 90th percentile → **95th percentile**
- `min_snr_db`: New requirement - **15 dB above noise floor**
- `min_duration`: 0.1s → **0.3s** (3x longer minimum)
- `freq_sweep_min`: 1000 Hz → **3000 Hz** (3x larger sweep required)
- Max chirps per file: 5 → **3** (only strongest peaks)

**New Quality Checks**:
- **Continuity check**: Rejects chirps where frequency changes are erratic
  - Calculates std_change and mean_change of frequency progression
  - Rejects if `std_change > 3 * mean_change` (too noisy)
- **SNR requirement**: Must be 15 dB above noise floor

**Impact**: Much stricter - only detects clear, long frequency sweeps

### 2. Click Train Detection (`detect_click_trains`)
**Goal**: Only detect sparse, sharp, high-amplitude dolphin echolocation clicks

**Parameter Updates**:
- `click_freq_range`: (10-150 kHz) → **(20-150 kHz)** (higher minimum)
- `min_clicks`: 5 → **10** (2x more clicks required per train)
- `threshold`: 95th percentile → **99th percentile**
- `noise_multiplier`: 5x → **8x** (must be 8x above noise level)
- `min_separation`: 1ms → **2ms** (clicks must be more distinct)
- `smoothing`: 1ms → **0.5ms** (preserve sharp edges)
- `filter_order`: 4 → **6** (sharper frequency cutoff)

**New Quality Checks**:
- **Prominence requirement**: Peaks must have prominence ≥ 30% of threshold
- **Width constraint**: Peaks must be between 1 sample and 5ms wide (rejects wide bumps)
- **Sharpness test**: Peak must dominate its local 4ms region (> 90th percentile locally)

**Impact**: Only detects clear, sharp, high-amplitude click sequences

### 3. Denoising Enhancement
**Update**: Added `hard_threshold=True` to wavelet denoising
- More aggressive noise removal before detection
- Removes more marginal signals that could trigger false positives

## Testing Results

### Test 1: 5 Files (Buoy210 directory)
- **Chirps**: 0% detection (0/5 files)
- **Click trains**: 100% detection (5/5 files)
- **Total click trains**: 38 (reduced from 186 in earlier test)
- **Total clicks**: 672 (reduced from 4019 in earlier test)

### Test 2: 20 Files (Buoy210 directory)
- **Chirps**: 0% detection (0/20 files)
- **Click trains**: 95% detection (19/20 files)
- **Total click trains**: 231
- **Total clicks**: 4148
- **Files with no detections**: 1/20 (5%)

### Test 3: 2 Files (Special directory)
- **Chirps**: 50% detection (1/2 files, 2 total chirps)
- **Click trains**: 100% detection (2/2 files)
- **Total click trains**: 58
- **Total clicks**: 1438

## Interpretation

The high detection rate in the Buoy210 directory (95-100%) may actually reflect genuine dolphin activity in that area. The key improvements are:

1. **Fewer false positives per file**: Reduced from 186 → 38 click trains in 5-file test
2. **Higher quality detections**: Only sharp, prominent, high-amplitude signals
3. **Chirp detection**: Now very conservative (0% in Buoy210, 50% in special files)
4. **Some files with no detections**: 1/20 files had no detections, showing selectivity works

## Algorithm Summary

### Chirp Detection Flow
1. Compute high-resolution spectrogram (nperseg=8192)
2. Apply 95th percentile + 15dB SNR threshold
3. Find ridges in time-frequency space
4. Check continuity (reject erratic frequency changes)
5. Require ≥0.3s duration and ≥3000 Hz sweep
6. Keep only top 3 strongest chirps

### Click Train Detection Flow
1. Bandpass filter to 20-150 kHz (higher order for sharpness)
2. Compute Hilbert envelope with minimal smoothing (0.5ms)
3. Apply 99th percentile + 8x noise level threshold
4. Find peaks with prominence, width, and separation constraints
5. Test sharpness (must dominate 4ms local region)
6. Group into trains with ≥10 clicks each
7. Require max 50ms inter-click interval

## Next Steps

1. Monitor the 1000-file production run (CLICK_CHIRP_001) results
2. Use `refresh_showcase.py` to visualize top detections
3. Validate that detected signals are genuine chirps/clicks
4. Adjust thresholds further if needed based on production results

## Files Modified

- `scripts/quick_find.py`:
  - Updated `detect_chirps()` function (lines ~28-178)
  - Updated `detect_click_trains()` function (lines ~177-308)
  - Updated function calls in main loop with new default parameters
  - Enhanced wavelet denoising with hard thresholding
