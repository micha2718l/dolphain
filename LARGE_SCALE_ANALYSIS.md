# Large-Scale EARS Data Analysis Pipeline

Complete workflow for finding and analyzing interesting dolphin acoustic data across massive datasets.

## Overview

This pipeline processes large collections of EARS files to automatically identify the most interesting recordings for research, publication, or further analysis. "Interesting" files are those with:

- **High whistle activity** - Lots of dolphin vocalizations
- **Good signal quality** - High SNR, clear signals
- **Diverse acoustics** - Multiple whistle types and frequency patterns
- **Minimal noise** - Clean recordings with low artifacts
- **High whistle-band energy** - Strong 5-25 kHz content

## The Pipeline

### Stage 0: Catalog Your Data

First, understand what you have on disk:

```bash
python crawl_data_drive.py
```

**Features:**

- Crawls entire drive recursively
- Counts files by directory and type
- Identifies all EARS files (any 3-digit extension)
- Tracks sizes and directory structure
- **Persistent progress** - pause with Ctrl+C, resume with `--resume`
- Saves every 60 seconds automatically

**Output:**

- `crawl_progress.json` - Resume checkpoint
- `data_drive_catalog.json` - Full catalog
- `data_drive_report.txt` - Human-readable summary

**Runtime:** ~1-10 minutes per 10,000 files (depends on disk speed)

---

### Stage 1-3: Find Interesting Files

Multi-stage filtering to identify the best files:

```bash
# Quick scan (10% sample) - RECOMMENDED FIRST RUN
python find_interesting_files.py --data-dir /Volumes/ladcuno8tb0/ --quick

# Full analysis (all files)
python find_interesting_files.py --data-dir /Volumes/ladcuno8tb0/

# Resume interrupted run
python find_interesting_files.py --data-dir /Volumes/ladcuno8tb0/ --resume
```

**Stage 1: Quick Scan** (FAST - ~0.5s per file)

- Basic spectral analysis
- Whistle-band power calculation
- Signal quality metrics
- Filters out ~80% of low-quality files

**Stage 2: Whistle Detection** (MEDIUM - ~1s per file)

- Full denoising
- Whistle detection and characterization
- SNR calculation
- Calculates "interestingness score"
- Takes top 10% to Stage 3

**Stage 3: Deep Analysis** (DETAILED - ~2s per file)

- Comprehensive spectral analysis
- Temporal segmentation
- Multi-band power distribution
- Activity patterns
- Final ranking

**Output:**

- `interesting_files_analysis/progress.json` - Resume checkpoint
- `interesting_files_analysis/interesting_files.json` - Full results
- `interesting_files_analysis/interesting_files_report.txt` - Summary

**Runtime Examples:**

- 1,000 files: ~10 minutes (quick mode)
- 10,000 files: ~2 hours (quick mode)
- 100,000 files: ~20 hours (quick mode)

---

### Stage 4: Batch Experiments

Run comprehensive analysis suite on selected files:

```bash
# All experiments on selected files
python batch_experiments.py --data-dir /path/to/interesting/files

# Specific experiments only
python batch_experiments.py --data-dir /path/to/data --experiments whistle spectral

# Quick sample test
python batch_experiments.py --data-dir /path/to/data --sample 0.1

# Resume interrupted run
python batch_experiments.py --data-dir /path/to/data --resume
```

**Experiments:**

1. **Basic Metrics** - RMS, peak, dynamic range, zero-crossing rate
2. **Whistle Detection** - Find and characterize all vocalizations
3. **Spectral Analysis** - Frequency distribution across bands
4. **Quality Assessment** - SNR, noise levels, signal statistics

**Output:**

- `batch_experiments_results/checkpoints/` - Resume checkpoints for each experiment
- `batch_experiments_results/results/*.csv` - Result tables
- `batch_experiments_results/summary_report.txt` - Overall summary

**Runtime:** ~1-2s per file per experiment

---

### Stage 5: Visual Exploration

Create publication-quality visualizations:

```bash
# Generate plots for top 10 files
python explore_interesting.py --results interesting_files_analysis/interesting_files.json

# Top 20 files
python explore_interesting.py --results interesting_files_analysis/interesting_files.json --top 20
```

**Generates:**

- **Comparison plot** - Overview of top files
- **Detailed plots** for each top file:
  - Raw and denoised waveforms
  - Spectrogram with whistle markers
  - Power spectral density
  - Temporal energy profile
- **Markdown report** with rankings and recommendations

**Output:**

- `interesting_files_analysis/visualizations/top_files_comparison.png`
- `interesting_files_analysis/visualizations/rank01_*.png` (etc.)
- `interesting_files_analysis/visualizations/detailed_report.md`

---

## Complete Workflow Example

```bash
# 1. Catalog your drive (understand what you have)
python crawl_data_drive.py
# Pause with Ctrl+C if needed, resume with:
python crawl_data_drive.py --resume

# 2. Find interesting files (quick mode first to test)
python find_interesting_files.py --data-dir /Volumes/ladcuno8tb0/ --quick

# 3. If quick mode looks good, run full analysis
python find_interesting_files.py --data-dir /Volumes/ladcuno8tb0/

# 4. Run batch experiments on top files
# First, copy top files to a working directory (optional but recommended)
# Or run directly on the filtered list
python batch_experiments.py --data-dir /Volumes/ladcuno8tb0/ --sample 0.01

# 5. Create visualizations
python explore_interesting.py --results interesting_files_analysis/interesting_files.json --top 20
```

---

## Key Features

### ✅ Persistent Progress

**Every script saves progress automatically:**

- Pause anytime with Ctrl+C
- Resume with `--resume` flag
- No work is lost
- Can stop/start across days

### ✅ Efficient Processing

- Multi-stage filtering reduces computation
- Quick scan eliminates bad files early
- Sample modes for testing (`--quick`, `--sample`)
- Intelligent caching and checkpointing

### ✅ Comprehensive Analysis

- 5+ different experiment types
- Multiple quality metrics
- Whistle detection and characterization
- Spectral and temporal analysis

### ✅ Production-Ready Output

- CSV files for further analysis
- JSON for programmatic access
- Publication-quality visualizations
- Markdown reports for sharing

---

## Interestingness Scoring

Files are scored 0-100 based on:

| Component            | Max Points | Criteria                                                 |
| -------------------- | ---------- | -------------------------------------------------------- |
| Whistle Activity     | 40         | Number of whistles detected (0.5 pts each, capped at 40) |
| Signal Quality (SNR) | 20         | SNR above 5 dB (2 pts per dB, capped at 20)              |
| Whistle Coverage     | 15         | % of time with whistles (0.15 pts per %, capped at 15)   |
| Whistle Band Power   | 15         | % power in 5-25 kHz (0.15 pts per %, capped at 15)       |
| Spectral Diversity   | 10         | Bandwidth above 5 kHz (1 pt per kHz, capped at 10)       |

**Top scores (>80):** Exceptional files - lots of clear whistles, high quality
**Good scores (60-80):** Strong candidates - clear activity, good quality
**Medium scores (40-60):** Moderate interest - some activity or quality issues
**Low scores (<40):** Probably not very interesting

---

## Performance Tips

### For Quick Testing

```bash
# Sample 10% of files
python find_interesting_files.py --data-dir /path/to/data --quick

# Or custom sample rate (1% = 0.01)
python find_interesting_files.py --data-dir /path/to/data --sample-rate 0.01
```

### For Large Datasets

```bash
# Run overnight, it will save progress automatically
nohup python find_interesting_files.py --data-dir /Volumes/ladcuno8tb0/ > analysis.log 2>&1 &

# Check progress
tail -f analysis.log

# If interrupted, resume
python find_interesting_files.py --data-dir /Volumes/ladcuno8tb0/ --resume
```

### Parallel Processing (future enhancement)

Currently processes files sequentially. Could add multiprocessing:

```python
# Future: --parallel 4 flag to use 4 CPU cores
```

---

## Troubleshooting

**"No files found"**

- Check drive is mounted: `ls /Volumes/ladcuno8tb0/`
- Check for EARS files: `find /Volumes/ladcuno8tb0/ -name "*.210" | head`

**"Out of memory"**

- Use `--quick` mode or smaller `--sample-rate`
- Process in batches by subdirectory

**"Progress not saving"**

- Check disk space
- Check write permissions in current directory

**Slow performance**

- External drives are slower than internal SSDs
- USB 2.0 is much slower than USB 3.0 or Thunderbolt
- Network drives can be very slow

---

## File Structure

```
dolphain/
├── crawl_data_drive.py          # Stage 0: Catalog drive
├── find_interesting_files.py    # Stage 1-3: Find best files
├── batch_experiments.py         # Stage 4: Run experiments
├── explore_interesting.py       # Stage 5: Visualize results
│
├── crawl_progress.json          # Catalog checkpoint
├── data_drive_catalog.json      # Drive catalog
├── data_drive_report.txt        # Catalog summary
│
├── interesting_files_analysis/
│   ├── progress.json            # Finding checkpoint
│   ├── interesting_files.json   # Detailed results
│   ├── interesting_files_report.txt
│   └── visualizations/
│       ├── top_files_comparison.png
│       ├── rank01_*.png
│       └── detailed_report.md
│
└── batch_experiments_results/
    ├── checkpoints/             # Experiment checkpoints
    ├── results/*.csv            # Data tables
    └── summary_report.txt       # Summary
```

---

## Next Steps After Analysis

Once you've found interesting files:

1. **Review visualizations** - Check top 20 plots
2. **Read detailed_report.md** - See recommendations
3. **Copy top files** to working directory for detailed study
4. **Run custom experiments** using `dolphain` library
5. **Create publication figures** from the best examples
6. **Share findings** - Reports are ready to share with collaborators

---

## Credits

Built using the `dolphain` library for EARS file processing and acoustic analysis.

See `TESTING_FRAMEWORK.md` for details on the underlying experiment framework.
