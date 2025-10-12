# 🐬 Large-Scale Analysis System - Quick Reference

## 🎯 What You Have Now

A complete pipeline to analyze **hundreds of thousands** of EARS files and automatically find the most interesting dolphin acoustic recordings.

## 🚀 Quick Start (Recommended)

**For fast results on 1000 random files:**

```bash
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000
```

This will:
- ✅ Sample 1000 files randomly from pre-generated list
- ✅ Run whistle detection on each
- ✅ Score them by interestingness
- ✅ Give you top 20 files in ~15-20 minutes

**Output:** `outputs/results/quick_find_results/top_20_files.txt`

---

## 📋 All Available Tools (in `scripts/`)

### 1. **`quick_find.py`** ⭐ START HERE
**Purpose:** Fast way to find interesting files  
**Speed:** ~1s per file  
**Best for:** Quick exploration, testing, getting immediate results

```bash
# Using pre-generated file list (RECOMMENDED - much faster!)
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000

# Or scan directory (slow on external drives)
python scripts/quick_find.py --data-dir /Volumes/ladcuno8tb0/ --n-files 1000
```

---

### 2. **`crawl_data_drive.py`**
**Purpose:** Catalog what's on your drive  
**Speed:** ~100-1000 files/second (just listing, not analyzing)  
**Best for:** Understanding your data structure, getting file counts

```bash
python scripts/crawl_data_drive.py
# Pause with Ctrl+C, resume with:
python scripts/crawl_data_drive.py --resume
```

**Already done! File list at:** `outputs/ears_files_list.txt` (949,504 files)

---

### 3. **`find_interesting_files.py`**
**Purpose:** 3-stage intelligent filtering of large datasets  
**Speed:** Stage 1: 0.5s/file, Stage 2: 1s/file, Stage 3: 2s/file  
**Best for:** When you want the BEST files from tens of thousands

```bash
# Using file list (RECOMMENDED)
python scripts/find_interesting_files.py --file-list outputs/ears_files_list.txt --quick

# Full analysis
python scripts/find_interesting_files.py --file-list outputs/ears_files_list.txt

# Resume if interrupted
python scripts/find_interesting_files.py --file-list outputs/ears_files_list.txt --resume
```

---

### 4. **`batch_experiments.py`**
**Purpose:** Run comprehensive analysis suite on selected files  
**Speed:** ~1-2s per file per experiment  
**Best for:** Detailed analysis of interesting files you've already identified

```bash
python scripts/batch_experiments.py --data-dir /path/to/selected/files
```

---

### 5. **`explore_interesting.py`**
**Purpose:** Create publication-quality visualizations  
**Best for:** Final presentation, sharing results, visual inspection

```bash
python scripts/explore_interesting.py --results outputs/results/interesting_files_analysis/interesting_files.json --top 20
```

---

### 6. **`visualize_random.py`** ⭐ SANITY CHECK
**Purpose:** Quick visual inspection of random files  
**Best for:** Verifying data quality, spot-checking results

```bash
python scripts/visualize_random.py --file-list outputs/ears_files_list.txt --n-files 8
```

**Output:** `outputs/plots/sanity_check_plots/sample_*.png`

---

### 7. **`ears_to_wav.py`** 🔊 AUDIO CONVERSION
**Purpose:** Convert EARS files to WAV for listening  
**Best for:** Hearing what the dolphins sound like!

```bash
python scripts/ears_to_wav.py /path/to/file.210
```

**Output:** `outputs/audio/FILENAME_raw.wav`, `outputs/audio/FILENAME_denoised.wav`

---

## 🎬 Recommended Workflows

### Workflow A: Fast Exploration (TODAY)
**Goal:** Find some cool files in the next hour

```bash
# 1. Quick find on 1000 files (~20 min)
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000

# 2. Check results
cat outputs/results/quick_find_results/top_20_files.txt

# 3. Convert to audio to listen
python scripts/ears_to_wav.py /Volumes/ladcuno8tb0/Buoy171/72146FB7.171

# 4. Visualize a few
python scripts/visualize_random.py --file-list outputs/ears_files_list.txt --n-files 5
```

---

### Workflow B: Comprehensive Analysis (OVERNIGHT)
**Goal:** Find the absolute best files from entire dataset

```bash
# 1. Start overnight analysis (quick mode = 10% sample)
nohup python scripts/find_interesting_files.py --file-list outputs/ears_files_list.txt --quick > analysis.log 2>&1 &

# 2. Check progress periodically
tail -f analysis.log

# 3. Next day: visualize results
python scripts/explore_interesting.py --results outputs/results/interesting_files_analysis/interesting_files.json --top 20
```

---

### Workflow C: Full Systematic Study (WEEK-LONG)
**Goal:** Process everything, create comprehensive dataset

```bash
# Day 1-2: Find interesting files (full dataset, not quick)
python scripts/find_interesting_files.py --file-list outputs/ears_files_list.txt

# Day 3: Batch experiments on top 1000
python scripts/batch_experiments.py --data-dir /path/to/top/1000/files

# Day 4: Create visualizations
python scripts/explore_interesting.py --results outputs/results/interesting_files_analysis/interesting_files.json --top 50
```

---

## 💡 Key Features

### ✅ Persistence Everywhere
**Every script saves progress automatically!**
- Ctrl+C to pause
- Add `--resume` to continue
- No lost work

### ✅ Smart Sampling
**Don't need to process everything:**
- `--quick` = 10% sample
- `--sample 0.01` = 1% sample
- `--n-files 1000` = exactly 1000 files

### ✅ Multiple Output Formats
- **JSON** - For programs/further analysis
- **CSV** - For Excel/pandas/R
- **TXT** - Human-readable reports
- **PNG** - Visualizations
- **MD** - Markdown documentation

---

## 📊 What Makes Files "Interesting"?

**Scored 0-100 based on:**

| Factor | Weight | What it measures |
|--------|--------|------------------|
| 🎵 Whistle Activity | 40% | Number of dolphin vocalizations |
| 📡 Signal Quality | 20% | SNR (signal-to-noise ratio) |
| ⏱️ Whistle Coverage | 15% | % of time with whistles |
| 🎼 Whistle Band Power | 15% | Energy in 5-25 kHz range |
| 🌈 Spectral Diversity | 10% | Frequency bandwidth |

**Top scores (>80):** 🌟 Exceptional - clear, lots of activity  
**Good scores (60-80):** ✅ Strong candidates  
**Medium (40-60):** 😐 Some interest  
**Low (<40):** 👎 Probably skip these

---

## 🔧 Troubleshooting

**"No files found"**
```bash
# Check drive is mounted
ls /Volumes/ladcuno8tb0/

# Check for EARS files
find /Volumes/ladcuno8tb0/ -name "*.[0-9][0-9][0-9]" | head -10
```

**"Running slowly"**
- External drives are slower than internal
- USB 2.0 is much slower than USB 3.0
- Try smaller samples first: `--n-files 100`
- **Use pre-generated file list!** Much faster than directory scanning

**"Out of memory"**
- Use sampling: `--quick` or `--sample 0.1`
- Process smaller subdirectories separately

**"Want to run in background"**
```bash
# Use nohup to run overnight
nohup python scripts/quick_find.py --file-list outputs/ears_files_list.txt > analysis.log 2>&1 &

# Check progress
tail -f analysis.log

# Check if still running
ps aux | grep python
```

---

## 📁 Output Structure

After running everything, you'll have:

```
outputs/
├── results/
│   ├── quick_find_results/          # From quick_find.py
│   │   ├── top_20_files.txt        # ⭐ Top files list
│   │   ├── all_results.csv
│   │   └── results.json
│   │
│   └── interesting_files_analysis/  # From find_interesting_files.py
│       ├── interesting_files_report.txt  # ⭐ Top files
│       ├── interesting_files.json
│       └── detailed_report.md        # ⭐ Recommendations
│
├── plots/
│   ├── sanity_check_plots/          # From visualize_random.py
│   │   └── sample_*.png
│   └── visualizations/              # From explore_interesting.py
│       ├── top_files_comparison.png  # ⭐ Overview plot
│       └── rank01_*.png              # ⭐ Detailed plots
│
├── audio/                           # From ears_to_wav.py
│   ├── *_raw.wav
│   └── *_denoised.wav
│
├── analysis_runs/                   # From batch_experiments.py
│   ├── results/*.csv
│   └── summary_report.txt       # ⭐ Experiment summary
│
├── ears_files_list.txt              # Master file list (949K files)
└── crawl_progress.json              # Catalog checkpoint
```

**Files marked ⭐ are the ones to check first!**

---

## 🎓 Next Steps

1. **Review your results** - Check the top 20 files
2. **Copy interesting files** to a working directory
3. **Use the dolphain library** for custom analysis:
   ```python
   import dolphain
   data = dolphain.read_ears_file('interesting_file.210')
   whistles = dolphain.detect_whistles(data['data'], data['sample_rate'])
   dolphain.plot_spectrogram(data['data'], data['sample_rate'])
   ```
4. **Create figures** for papers/presentations
5. **Run experiments** - See `examples/experiment_templates.ipynb`

---

## 📚 Documentation

- **`LARGE_SCALE_ANALYSIS.md`** - Full detailed guide
- **`TESTING_FRAMEWORK.md`** - Experiment framework docs
- **`TESTING_QUICK_START.md`** - Framework quick start
- **`README.md`** - Library overview

---

## ⏱️ Time Estimates

| Task | Files | Time |
|------|-------|------|
| Catalog drive | 100,000 | 5-10 min |
| Quick find | 1,000 | 15-20 min |
| Quick find | 10,000 | 3-4 hours |
| Full interesting search (quick mode) | 100,000 | 20-24 hours |
| Batch experiments | 1,000 | 30-60 min |
| Create visualizations | top 20 | 5-10 min |

---

## 💪 You're Ready!

**Start here:**
```bash
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000
```

**Check results in ~20 minutes:**
```bash
cat outputs/results/quick_find_results/top_20_files.txt
```

**Listen to a file:**
```bash
python scripts/ears_to_wav.py /Volumes/ladcuno8tb0/Buoy171/72146FB7.171
open outputs/audio/72146FB7_denoised.wav
```

**Visualize random files:**
```bash
python scripts/visualize_random.py --file-list outputs/ears_files_list.txt --n-files 5
open outputs/plots/sanity_check_plots/
```

**That's it!** 🎉

The scripts handle all the complex stuff:
- ✅ Denoising
- ✅ Whistle detection  
- ✅ Quality assessment
- ✅ Scoring and ranking
- ✅ Progress saving
- ✅ Error handling

You just pick the best files and do science! 🐬🔬
