# ✅ Export Script Fixed and Working!

## 🎉 Success!

The `export_top_files.py` script is now fully functional and tested!

## 🐛 Issues Fixed

1. **Wrong parameter name**: `wavelet_denoise()` doesn't accept `level` parameter

   - Fixed: Removed `level=5` parameter
   - Changed wavelet to `'db20'` (default, better quality)

2. **Wrong whistle keys**: Used `freq_min`/`freq_max` instead of `min_freq`/`max_freq`
   - Fixed: Updated all references to use correct keys from `detect_whistles()` output

## ✅ Tested and Working

Successfully exported 3 files with:

- ✅ Detailed 6-panel plots (3 files × ~1MB each)
- ✅ Raw WAV files (3 files × 7.8MB each)
- ✅ Denoised WAV files (3 files × 7.8MB each)
- ✅ Summary README.txt

## 🚀 Usage

### Export current top 5 from your running analysis:

```bash
source .venv/bin/activate
python scripts/export_top_files.py --checkpoint outputs/results/large_run/checkpoint.json --top 5
```

### Export from completed results:

```bash
python scripts/export_top_files.py --checkpoint outputs/results/large_run/results.json --top 5
```

### Export top 10:

```bash
python scripts/export_top_files.py --checkpoint outputs/results/large_run/checkpoint.json --top 10
```

## 📊 What You Get

Each export creates:

```
outputs/exports/<name>/
├── audio/
│   ├── <filename>_raw.wav         # Original audio
│   ├── <filename>_denoised.wav    # Cleaned audio
│   └── ... (2 files per top file)
│
├── plots/
│   ├── rank01_<filename>.png      # 6-panel visualization
│   ├── rank02_<filename>.png
│   └── ... (1 plot per top file)
│
└── README.txt                      # Summary of all files
```

## 📈 Each Plot Contains:

1. **Raw Waveform** - Original signal over time
2. **Denoised Waveform** - After wavelet denoising
3. **Raw Spectrogram** - Full frequency spectrum (0-50 kHz)
4. **Denoised Spectrogram** - After cleaning (0-50 kHz)
5. **Whistle Detection** - Zoomed to 5-25 kHz with red boxes around detected whistles
6. **Statistics Panel** - File info, scores, whistle count, and details

## 🎯 Quick Commands

### View your exports:

```bash
# Open plots
open outputs/exports/test_fixed2/plots/

# Listen to audio
open outputs/exports/test_fixed2/audio/

# Read summary
cat outputs/exports/test_fixed2/README.txt
```

### Export snapshots while analysis runs:

```bash
# Every 30 minutes, export current top 5 to see evolution
python scripts/export_top_files.py \
  --checkpoint outputs/results/large_run/checkpoint.json \
  --top 5 \
  --output-dir outputs/exports/snapshot_$(date +%H%M)
```

## 💡 Pro Tips

1. **Monitor + Export**: Run both simultaneously

   ```bash
   # Terminal 1: Monitor
   python scripts/monitor_quick_find.py --output-dir outputs/results/large_run

   # Terminal 2: Export when you see something interesting
   python scripts/export_top_files.py --checkpoint outputs/results/large_run/checkpoint.json --top 5
   ```

2. **Auto-find checkpoint**: If run from project root, it searches common locations

   ```bash
   python scripts/export_top_files.py --top 5
   ```

3. **Compare runs**: Export to different directories
   ```bash
   python scripts/export_top_files.py --checkpoint run1/checkpoint.json --output-dir exports/run1
   python scripts/export_top_files.py --checkpoint run2/checkpoint.json --output-dir exports/run2
   ```

## 📦 File Sizes

Per file:

- Raw WAV: ~7.8 MB (21.3 seconds at 192 kHz)
- Denoised WAV: ~7.8 MB
- Plot PNG: ~1 MB (high quality, 150 DPI)

For top 5:

- Audio: ~78 MB (10 WAV files)
- Plots: ~5 MB (5 PNG files)
- **Total: ~83 MB**

## 🐬 Ready to Use!

The script is now fully tested and working. You can export your top files anytime during or after the analysis!

```bash
source .venv/bin/activate
python scripts/export_top_files.py --checkpoint outputs/results/large_run/checkpoint.json --top 5
```

Happy analyzing! 🔬🎵🐬
