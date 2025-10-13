# 🎵 Chirp & Click Train Detection

## Overview

The `quick_find.py` script has been **completely reworked** to focus on detecting two key acoustic features:

1. **🎵 Chirp Signals** - Frequency sweeps visible in spectrograms

   - Can come from various sources (fish, equipment, biological, etc.)
   - Characterized by continuous frequency modulation (sweeps up or down)
   - Detected by tracking frequency ridges across time in spectrogram

2. **🔊 Click Trains** - Rapid high-frequency clicks from dolphins
   - Used for echolocation by dolphins
   - Typically 10-150 kHz frequency range
   - Inter-click intervals (ICI) of 5-50 milliseconds
   - Detected using envelope analysis of high-frequency bands

## Key Changes from Previous Version

### Previous Version (Whistle-Based)

- Focused on detecting dolphin whistles (2-20 kHz)
- Scored based on whistle count, duration, diversity, FM rate, patterns, overlaps
- Good for finding communication sounds

### New Version (Chirp & Click Train)

- **Chirps**: Tracks frequency sweeps of any source
  - Minimum sweep of 500 Hz required
  - Minimum duration 50 ms
  - Scored on sweep range, rate, and diversity
- **Click Trains**: Detects rapid high-frequency clicks
  - 10-150 kHz frequency range (adjusted to sampling rate)
  - Minimum 5 clicks per train
  - Maximum 50 ms between clicks (inter-click interval)
  - Scored on regularity, count, and rate

## Detection Algorithms

### Chirp Detection

```
1. Compute high-resolution spectrogram
2. Apply power threshold (80th percentile)
3. Track frequency contours across time
4. Allow sweep up or down
5. Filter by minimum sweep range and duration
6. Extract sweep characteristics (rate, range, etc.)
```

### Click Train Detection

```
1. Band-pass filter to click frequency range (10-150 kHz)
2. Compute Hilbert envelope
3. Find peaks in envelope (potential clicks)
4. Group peaks into trains based on ICI
5. Calculate train statistics (rate, regularity, etc.)
```

## Scoring System (0-100 points)

### Chirp Scoring (40 points)

- **Basic count** (15 pts): More chirps = higher score
- **Quality** (15 pts):
  - Large frequency sweeps (up to 10 pts)
  - Fast sweep rates (up to 5 pts)
- **Diversity** (10 pts): Variety in start frequencies

### Click Train Scoring (40 points)

- **Train count** (10 pts): Number of detected trains
- **Click count** (10 pts): Total clicks across all trains
- **Regularity** (10 pts): Consistent inter-click intervals
- **Rate quality** (10 pts): Optimal rate 20-200 clicks/sec

### Signal Quality (20 points)

- SNR in high-frequency bands (5-50 kHz signal vs 0.5-2 kHz noise)

## Usage

### Basic Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run on sample of files
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 100

# Run on larger sample
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000

# Resume if interrupted
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000 --resume
```

### Output Files

The script creates these files in `quick_find_results/` (or custom `--output-dir`):

1. **`results.json`** - Full results with all metrics
2. **`top_20_files.txt`** - Top 20 files ranked by interestingness
3. **`all_results.csv`** - Spreadsheet with all files and metrics
4. **`checkpoint.json`** - Progress checkpoint (deleted on completion)

### Output Columns

CSV contains these columns:

- `file` - Full path to EARS file
- `filename` - Just the filename
- `recording_duration` - Total recording length (seconds)
- `n_chirps` - Number of detected chirps
- `chirp_coverage_percent` - % of time with chirps
- `mean_chirp_duration` - Average chirp duration
- `mean_freq_sweep` - Average frequency sweep (Hz)
- `n_click_trains` - Number of detected click trains
- `total_clicks` - Total clicks across all trains
- `click_train_coverage_percent` - % of time with click trains
- `mean_click_train_duration` - Average train duration
- `mean_click_rate` - Average clicks per second
- `mean_ici` - Average inter-click interval
- `interestingness_score` - Overall score (0-100)

## Progress Display

During processing, you'll see:

```
⏳ Progress: 50/1000 (5.0%) | 2.3 files/s | ETA: 6.9m
   Chirps: 45% | Clicks: 32% | Both: 12 | Checkpoint saved ✓
```

- **Chirps**: % of files with detected chirps
- **Clicks**: % of files with detected click trains
- **Both**: Number of files with both features

## Backup

The old whistle-based version has been backed up to:

```
scripts/quick_find_whistles_backup.py
```

You can restore it if needed.

## Next Steps

After running `quick_find.py`:

1. **Review results**:

   ```bash
   cat quick_find_results/top_20_files.txt
   ```

2. **Open CSV in spreadsheet** to sort/filter by specific features:

   ```bash
   open quick_find_results/all_results.csv
   ```

3. **Visualize top files**:

   ```bash
   # Get the top file path
   TOP_FILE=$(head -n 13 quick_find_results/top_20_files.txt | tail -n 1 | cut -d' ' -f2-)

   # Convert and plot
   python scripts/ears_to_wav.py "$TOP_FILE" --plot
   ```

## Parameter Tuning

You can adjust detection parameters by editing the function calls in `quick_find.py`:

### Chirp Parameters

```python
chirps = detect_chirps(
    signal_clean,
    data_dict["fs"],
    nperseg=2048,           # FFT window size (larger = better freq resolution)
    min_duration=0.05,      # Minimum chirp duration (seconds)
    freq_sweep_min=500      # Minimum frequency sweep (Hz)
)
```

### Click Train Parameters

```python
click_trains = detect_click_trains(
    signal_clean,
    data_dict["fs"],
    click_freq_range=(10000, 150000),  # Frequency range for clicks
    min_clicks=5,                       # Minimum clicks per train
    max_ici=0.05                        # Maximum inter-click interval (seconds)
)
```

## Technical Details

### Why These Features?

- **Chirps**: Broad acoustic feature that can indicate:
  - Biological activity (fish sounds)
  - Equipment/vessel sounds
  - Other interesting acoustic events
  - Potential dolphin vocalizations
- **Click Trains**: Specifically targets:
  - Dolphin echolocation
  - High-quality acoustic environment
  - Active foraging behavior
  - Navigation/exploration

### Frequency Ranges

- **Chirps**: No fixed range - detected across full spectrum
- **Click Trains**: 10-150 kHz (adjusted to Nyquist frequency)
- **Dolphin clicks**: Typically peak at 40-130 kHz
- **Sampling rate**: EARS files are typically 80 kHz (Nyquist = 40 kHz)

## Ready to Run!

When you're ready:

1. **Connect your external hard drive**
2. **Ensure you have the file list**: `outputs/ears_files_list.txt`
3. **Run the script** with desired sample size
4. **Let it run!** - Safe to interrupt and resume anytime

```bash
source .venv/bin/activate
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000
```

🐬 Happy chirp and click hunting!
