# 📊 Live Monitoring Guide

While `quick_find.py` is running in one terminal, you can monitor its progress in another terminal!

## 🎨 Option 1: Graphical Monitor (Recommended)

**Beautiful live-updating graphs with matplotlib:**

```bash
# In a separate terminal (activate venv first!)
source .venv/bin/activate
python scripts/monitor_quick_find.py --output-dir outputs/results/large_run
```

**Features:**

- 📊 Bar chart of top 5 files
- 🎯 Scatter plot (whistles vs coverage)
- 📈 Live statistics panel
- 🔄 Auto-refreshes every 5 seconds
- 🎨 Color-coded by rank

**Custom refresh rate:**

```bash
python scripts/monitor_quick_find.py --output-dir outputs/results/large_run --refresh 2
```

**Single snapshot (no auto-refresh):**

```bash
python scripts/monitor_quick_find.py --output-dir outputs/results/large_run --once
```

---

## 📟 Option 2: Text Monitor (Terminal Only)

**Simple text-based display (no matplotlib required):**

```bash
# In a separate terminal (activate venv first!)
source .venv/bin/activate
python scripts/monitor_text.py --output-dir outputs/results/large_run
```

**Features:**

- 📊 ASCII bar charts
- 🏆 Top 5 files list
- 📈 Progress statistics
- 🔄 Auto-refreshes every 5 seconds
- ⚡ Lightweight - runs in terminal

**Custom refresh rate:**

```bash
python scripts/monitor_text.py --output-dir outputs/results/large_run --refresh 2
```

---

## 🚀 Quick Start

### Terminal 1: Run Analysis

```bash
cd /Users/mjhaas/code/dolphain
source .venv/bin/activate
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 10000 --output-dir outputs/results/large_run
```

### Terminal 2: Monitor Progress

```bash
cd /Users/mjhaas/code/dolphain
source .venv/bin/activate

# Graphical (recommended)
python scripts/monitor_quick_find.py --output-dir outputs/results/large_run

# OR text-based
python scripts/monitor_text.py --output-dir outputs/results/large_run
```

---

## 📊 What You'll See

### Graphical Monitor:

```
┌─────────────────────────────────────────────────────┐
│          Top 5 Files (Live) - 234 files             │
│  #1 72123440.201    ████████████████████ 77.9       │
│  #2 71921D06.171    ███████████████████  76.4       │
│  #3 71824383.140    ████                 18.7       │
├─────────────────────────────────────────────────────┤
│  Scatter Plot          │  Statistics                │
│  (Whistles vs Coverage)│  Files: 234                │
│                        │  Hit Rate: 67%             │
│                        │  Mean Whistles: 23.4       │
└─────────────────────────────────────────────────────┘
```

### Text Monitor:

```
================================================================================
🐬 QUICK FIND LIVE MONITOR (Text Mode)
================================================================================
Watching: outputs/results/large_run/checkpoint.json
Press Ctrl+C to stop
Last refresh: 14:23:45
================================================================================

📊 PROGRESS STATISTICS
--------------------------------------------------------------------------------
  Files Processed:       234
  Files with Whistles:   156 (66.7%)
  Mean Whistles/File:    23.4
  Errors:                0

🏆 TOP 5 FILES (LIVE)
--------------------------------------------------------------------------------
#1. 72123440.201
    Score:  77.9 ████████████████████████████████████████
    Whistles:  71 | Coverage:  74.8%

#2. 71921D06.171
    Score:  76.4 ███████████████████████████████████████░
    Whistles:  65 | Coverage:  79.6%

#3. 71824383.140
    Score:  18.7 █████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
    Whistles:  14 | Coverage:  33.1%
...
```

---

## ⚙️ Options

| Flag           | Description                                  | Default              |
| -------------- | -------------------------------------------- | -------------------- |
| `--output-dir` | Directory where quick_find saves checkpoint  | `quick_find_results` |
| `--refresh`    | Seconds between updates                      | `5`                  |
| `--once`       | Single snapshot (monitor_quick_find.py only) | `False`              |

---

## 💡 Pro Tips

### 1. Match the Output Directory

Make sure the `--output-dir` matches between `quick_find.py` and the monitor:

```bash
# quick_find.py
--output-dir outputs/results/large_run

# monitor script
--output-dir outputs/results/large_run
```

### 2. Adjust Refresh Rate

```bash
# Fast refresh (every 2 seconds) - more up-to-date
python scripts/monitor_quick_find.py --output-dir outputs/results/large_run --refresh 2

# Slow refresh (every 30 seconds) - less CPU usage
python scripts/monitor_quick_find.py --output-dir outputs/results/large_run --refresh 30
```

### 3. Use Text Monitor for Remote Sessions

If you're SSH'ed into a server, use the text monitor:

```bash
python scripts/monitor_text.py --output-dir outputs/results/large_run
```

### 4. Take Snapshots

```bash
# Quick peek without blocking terminal
python scripts/monitor_quick_find.py --output-dir outputs/results/large_run --once
```

---

## 🔧 Troubleshooting

**"No checkpoint file found"**

- Quick_find hasn't started yet or hasn't processed 10 files
- Check that `--output-dir` matches
- Wait 10-20 seconds for first checkpoint

**"Waiting for checkpoint file..."**

- Normal! Appears before quick_find creates checkpoint
- Will update automatically once checkpoint exists

**Plot window doesn't update**

- Close and restart the monitor
- Try text monitor instead

**Monitor crashes**

- Make sure matplotlib is installed: `pip install matplotlib`
- Use text monitor if matplotlib issues persist

---

## 🎓 Example Session

```bash
# Terminal 1: Start analysis
$ python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000 --output-dir outputs/results/test_run

# Terminal 2: Start monitor
$ python scripts/monitor_quick_find.py --output-dir outputs/results/test_run

# Watch the top 5 change as more files are analyzed!
# The monitor will show:
# - Current top 5 files
# - How scores evolve
# - Hit rate percentage
# - Processing speed

# Press Ctrl+C in Terminal 2 when you want to stop monitoring
# (quick_find will keep running in Terminal 1)
```

---

## 🐬 Ready to Monitor!

Now you can watch your analysis in real-time and see which files are winning! 🏆

**Start monitoring:**

```bash
python scripts/monitor_quick_find.py --output-dir outputs/results/large_run
```

Or for text-only:

```bash
python scripts/monitor_text.py --output-dir outputs/results/large_run
```
