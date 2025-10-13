# 🎯 Quick Find Algorithm - Chirp & Click Train Detection

## Summary

The `quick_find.py` script has been **completely reworked** to detect:

1. **🎵 Chirp Signals** - Frequency sweeps (from any source)
2. **🔊 Click Trains** - Rapid high-frequency clicks (dolphin echolocation)

## What Changed

### Old Algorithm
- Detected dolphin **whistles** (2-20 kHz narrowband FM signals)
- Scored on whistle count, diversity, complexity, patterns, overlaps
- Good for finding dolphin communication

### New Algorithm  
- Detects **chirps** - any frequency sweep in the spectrogram
- Detects **click trains** - rapid high-frequency pulses (10-150 kHz)
- Scores on chirp quality (sweep range/rate) and click regularity
- Better for finding echolocation and diverse acoustic events

## Files

- **`scripts/quick_find.py`** - New chirp/click detection version
- **`scripts/quick_find_whistles_backup.py`** - Old whistle version (backup)
- **`CHIRP_CLICK_DETECTION.md`** - Full documentation

## Status

✅ **READY TO RUN**

The script is tested and working. Key features:
- Chirp detection working (tracks frequency sweeps)
- Click train detection working (finds rapid pulses, calculates ICI)
- Scoring system complete (0-100 points)
- Checkpointing enabled (resume anytime)
- Progress tracking with stats

## Quick Start

When you reconnect the hard drive:

```bash
# Activate environment
source .venv/bin/activate

# Run on small sample first (test)
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 10

# Run on larger sample
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000

# Can interrupt anytime and resume:
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000 --resume
```

## Output

Results saved to `quick_find_results/`:
- `results.json` - Full results
- `top_20_files.txt` - Top ranked files
- `all_results.csv` - Spreadsheet with metrics
- `checkpoint.json` - Progress (auto-deleted when done)

## Metrics Tracked

For each file:
- **Chirps**: count, coverage%, duration, frequency sweep
- **Click trains**: count, total clicks, coverage%, rate, ICI
- **Score**: 0-100 (chirp quality 40pts + click quality 40pts + SNR 20pts)

## What to Expect

During processing you'll see files categorized by:
- Files with chirps (%)
- Files with click trains (%)  
- Files with both features

Top files will have:
- Large frequency sweeps (chirps)
- Regular click trains with proper ICI
- High SNR in relevant bands

## Next Steps

After running, review results and visualize top files to confirm the detections are meaningful. You may want to adjust parameters based on what you find.

🐬 Ready when you are!
