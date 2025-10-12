# 🐬 DOLPHAIN Large-Scale Analysis Pipeline

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     YOUR EXTERNAL DRIVE                             │
│                  /Volumes/ladcuno8tb0/                              │
│                                                                     │
│  📁 Buoy001/                                                        │
│     ├── *.210, *.211, *.212 ... (EARS files)                       │
│  📁 Buoy002/                                                        │
│  📁 Buoy003/                                                        │
│  📁 ...                                                             │
│  └── 📁 BuoyNNN/                                                    │
│                                                                     │
│  Total: 10,000 - 1,000,000+ EARS files                             │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    STAGE 0: CATALOG                                 │
│                 crawl_data_drive.py                                 │
│                                                                     │
│  • Recursively scans entire drive                                   │
│  • Counts files by directory                                        │
│  • Identifies all EARS files                                        │
│  • Calculates sizes                                                 │
│  • Saves progress every 60s                                         │
│                                                                     │
│  Speed: ~100-1000 files/sec                                         │
│  Output: data_drive_catalog.json, report.txt                        │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
          ┌─────────────────┐  ┌──────────────────┐
          │  QUICK PATH ⚡  │  │  THOROUGH PATH 🔬 │
          └─────────────────┘  └──────────────────┘
                    ↓                   ↓
                    ↓                   ↓
┌─────────────────────────────┐ ┌──────────────────────────────────────┐
│    quick_find.py            │ │  find_interesting_files.py           │
│                             │ │                                      │
│  • Sample N files randomly  │ │  STAGE 1: Quick Scan (0.5s/file)     │
│  • Run whistle detection    │ │  • Spectral analysis                 │
│  • Calculate scores         │ │  • Whistle-band power                │
│  • Rank by interest         │ │  • Filter ~80% of files              │
│                             │ │                                      │
│  Time: 15-20 min for 1000   │ │  STAGE 2: Whistle Detection (1s/file)│
│  Output: top_20_files.txt   │ │  • Full denoising                    │
│                             │ │  • Whistle characterization          │
│  ⭐ RECOMMENDED FOR QUICK   │ │  • Interestingness scoring           │
│     EXPLORATION             │ │  • Keep top 10%                      │
└─────────────────────────────┘ │                                      │
                                │  STAGE 3: Deep Analysis (2s/file)    │
                                │  • Multi-band spectral               │
                                │  • Temporal patterns                 │
                                │  • Final ranking                     │
                                │                                      │
                                │  Time: 20+ hours (quick mode)        │
                                │  Output: interesting_files.json      │
                                │                                      │
                                │  ⭐ BEST FOR COMPREHENSIVE STUDY     │
                                └──────────────────────────────────────┘
                    ↓                                ↓
                    └────────────┬─────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                  SELECTED INTERESTING FILES                         │
│                     (Top 20-1000 files)                             │
│                                                                     │
│  Characteristics:                                                   │
│  ✓ High whistle activity (10-100+ whistles)                        │
│  ✓ Good signal quality (SNR > 10 dB)                               │
│  ✓ Substantial coverage (>20% with whistles)                       │
│  ✓ Clear acoustic features                                          │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
                    ┌────────────┴────────────┐
                    ↓                         ↓
┌──────────────────────────────┐  ┌──────────────────────────────────┐
│  batch_experiments.py        │  │  explore_interesting.py          │
│                              │  │                                  │
│  COMPREHENSIVE ANALYSIS:     │  │  VISUALIZATION & REVIEW:         │
│  1. Basic Metrics            │  │  • Comparison plots              │
│  2. Whistle Detection        │  │  • Detailed spectrograms         │
│  3. Spectral Analysis        │  │  • Waveforms + whistles          │
│  4. Quality Assessment       │  │  • Power spectral density        │
│                              │  │  • Temporal profiles             │
│  Output: CSV tables,         │  │  • Publication-ready figures     │
│          summary reports     │  │                                  │
│                              │  │  Output: PNG plots,              │
│  Time: 1-2 hours for 1000    │  │          markdown reports        │
└──────────────────────────────┘  └──────────────────────────────────┘
                    ↓                         ↓
                    └────────────┬────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        FINAL OUTPUTS                                │
│                                                                     │
│  📊 Data Tables (CSV/JSON)                                          │
│     • All metrics for every file                                    │
│     • Rankings and scores                                           │
│     • Ready for statistical analysis                                │
│                                                                     │
│  📈 Visualizations (PNG)                                            │
│     • Spectrograms with whistle detections                          │
│     • Comparison charts                                             │
│     • Quality figures for publication                               │
│                                                                     │
│  📝 Reports (TXT/MD)                                                │
│     • Top files list with full paths                                │
│     • Summary statistics                                            │
│     • Recommendations for further study                             │
│                                                                     │
│  🎯 TOP FILES IDENTIFIED                                            │
│     • Best for publication                                          │
│     • Best for presentations                                        │
│     • Best examples for methods papers                              │
│     • Training data for ML models                                   │
└─────────────────────────────────────────────────────────────────────┘
                                 ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      YOUR RESEARCH! 🔬                              │
│                                                                     │
│  • Detailed acoustic analysis                                       │
│  • Behavior correlation studies                                     │
│  • Method development                                               │
│  • Machine learning training                                        │
│  • Publication figures                                              │
│  • Conference presentations                                         │
└─────────────────────────────────────────────────────────────────────┘
```

## Key Features at Every Stage

### 💾 Persistence
Every script saves progress automatically:
- Pause anytime (Ctrl+C)
- Resume with `--resume`
- No lost work

### ⚡ Smart Filtering
Multi-stage pipeline reduces computation:
- Stage 1: 100,000 → 20,000 (80% filtered)
- Stage 2: 20,000 → 2,000 (90% filtered)  
- Stage 3: 2,000 → deep analysis

### 🎯 Flexible Sampling
Don't need to process everything:
- `--quick`: 10% sample
- `--sample 0.01`: 1% sample
- `--n-files 1000`: Exactly 1000 files

### 📊 Multiple Outputs
Choose your format:
- JSON (programmatic)
- CSV (Excel/pandas)
- TXT (human-readable)
- PNG (visualizations)
- MD (documentation)

## Processing Times

```
Files Processed    Quick Path    Thorough Path
─────────────────────────────────────────────
      1,000          20 min         2 hours
     10,000         3 hours        20 hours
    100,000           N/A          8 days*
    
    *Use quick mode (10% sample) → 1 day
```

## Storage Requirements

```
Stage             Per File    1,000 Files    10,000 Files
──────────────────────────────────────────────────────────
EARS Files        ~50 KB        50 MB          500 MB
Stage 1 Results   ~500 B       500 KB           5 MB
Stage 2 Results   ~1 KB          1 MB          10 MB
Stage 3 Results   ~2 KB          2 MB          20 MB
Visualizations    ~500 KB      500 MB           5 GB
                                (top 20)      (top 200)
```

## CPU Usage

- **Single-threaded** (current)
- **~1 CPU core** at 100%
- Can run in background
- Future: Multi-core support

## Recommended Hardware

**Minimum:**
- 2 CPU cores
- 4 GB RAM
- 10 GB free disk space

**Recommended:**
- 4+ CPU cores
- 8+ GB RAM  
- 100+ GB free disk space
- USB 3.0+ or Thunderbolt for external drive

**Optimal:**
- 8+ CPU cores
- 16+ GB RAM
- SSD for results storage
- External SSD for data (not HDD)

---

Made with 🐬 using the dolphain library
