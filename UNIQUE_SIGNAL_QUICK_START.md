# 🌟 Unique Signal Detection - Quick Start

**Branch:** `feature/unique-signal-detection`  
**Status:** Ready to run!

---

## 🚀 Run the Experiment

```bash
cd /Users/mjhaas/code/dolphain

# Already on feature branch - just run it!
python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --mode unique \
  --output-dir experiments/unique_signals
```

---

## 🎯 What It Finds

Exceptional acoustic features:
- 🚀 Ultra-fast frequency sweeps (>10 kHz/sec)
- 🎚️ Extreme frequency ranges (>50 kHz span)
- 🎼 Multiple simultaneous vocalizations
- 🥁 Unusual click patterns (bursts, rhythms)
- 🎹 Harmonic structures (overtones)
- 🌈 High spectral diversity (5 frequency bands)

---

## 📊 Key Differences

### vs. Standard Mode
| Feature | Standard Mode | Unique Mode |
|---------|--------------|-------------|
| **Focus** | Quantity (count detections) | Quality (exceptional features) |
| **Scoring** | Chirps + clicks + SNR | Rarity + diversity + extremes |
| **Use Case** | Find any vocalizations | Find gems in dataset |
| **Output** | n_chirps, n_click_trains | uniqueness_score, feature metrics |

### Scoring
- **Standard:** Interestingness (0-100) - how active is the file?
- **Unique:** Uniqueness (0-100) - how rare/exceptional are the features?

---

## 📁 Output

Saves to `experiments/unique_signals/` (gitignored):
- `results.json` - Full results with all metrics
- `top_20_files.txt` - Most unique files
- `all_results.csv` - Spreadsheet format
- `checkpoint.json` - Resume point

---

## 🎨 Generate Showcase

After analysis:

```bash
python scripts/refresh_showcase.py \
  --results-dir experiments/unique_signals \
  --top 15 \
  --output site/showcase

cd site && python3 -m http.server 8000
# Open: http://localhost:8000/showcase.html
```

---

## 📖 Full Documentation

See `UNIQUE_SIGNAL_DETECTION.md` for:
- Complete feature descriptions
- Scoring breakdown
- Expected results
- Interpretation guide

---

## ✅ Clean Implementation

- ✅ Integrated into existing `quick_find.py`
- ✅ Uses same framework (checkpoints, resume, progress)
- ✅ No code duplication
- ✅ Simple `--mode` flag to switch
- ✅ Compatible with all existing tools (refresh_showcase, etc.)

---

**Ready to find the most amazing sounds in your dataset!** 🐬🌟
