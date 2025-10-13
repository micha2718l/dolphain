# 🚀 Quick Find Improvements

## What's New

I've enhanced `quick_find.py` with **checkpointing** and **better status updates**!

## ✨ New Features

### 1. **Checkpointing (Resume on Interruption)**

- ✅ Saves progress every 10 files
- ✅ Safe to interrupt anytime (Ctrl+C)
- ✅ Resume with `--resume` flag
- ✅ Checkpoint automatically deleted when complete

### 2. **Better Status Updates**

- ✅ Progress updates every 10 files (instead of 50)
- ✅ Shows **hit rate** (% of files with whistles)
- ✅ Shows when checkpoint is saved
- ✅ More emoji indicators 🐬📋🔍📊⏳✅

### 3. **Random Sampling**

- ✅ Yes, it samples randomly from the file list
- ✅ Uses `random.sample()` for unbiased selection

## 🎯 Usage

### Basic Run

```bash
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000
```

### Safe Interruption

```bash
# Start processing
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000

# Press Ctrl+C anytime to stop (progress is saved!)

# Resume later
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000 --resume
```

### Custom Output

```bash
python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 5000 \
  --output-dir outputs/results/large_run \
  --resume
```

## 📊 Example Output

```
================================================================================
🐬 QUICK FIND - INTERESTING EARS FILES
================================================================================
Sample size: 1000 files
Output: outputs/results/quick_find_results

📋 Step 1: Loading EARS file list...
  Reading from: outputs/ears_files_list.txt
  Loaded 949504 files from list
  Sampling 1000 files randomly
  Time: 1.0s

🔍 Step 2: Running quick analysis...
  Will save checkpoint every 10 files (safe to interrupt!)
  📊 Status: 0/1000 files already processed
  🚀 Processing 1000 remaining files...

  ⏳ Progress: 10/1000 (1.0%) | 0.7 files/s | ETA: 23.5m | Hit rate: 80% | Checkpoint saved ✓
  ⏳ Progress: 20/1000 (2.0%) | 0.8 files/s | ETA: 20.4m | Hit rate: 75% | Checkpoint saved ✓
  ⏳ Progress: 30/1000 (3.0%) | 0.9 files/s | ETA: 18.0m | Hit rate: 70% | Checkpoint saved ✓
  ...
```

## 🔍 What It Shows

| Column             | Meaning                            |
| ------------------ | ---------------------------------- |
| Progress           | Files completed / Total files      |
| %                  | Percentage complete                |
| files/s            | Processing speed                   |
| ETA                | Estimated time remaining           |
| Hit rate           | % of files with whistles so far    |
| Checkpoint saved ✓ | Progress is saved (safe to Ctrl+C) |

## 💡 Pro Tips

### 1. Test First with Small Sample

```bash
# Test with 10 files first (~10 seconds)
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 10
```

### 2. Run Overnight for Large Batches

```bash
# Start a large run in background
nohup python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 10000 \
  --resume \
  > large_run.log 2>&1 &

# Check progress anytime
tail -f large_run.log
```

### 3. Resume After Interruption

```bash
# If you interrupt or it crashes, just add --resume
python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --resume
```

### 4. Multiple Runs Don't Conflict

```bash
# Use different output directories for parallel runs
python scripts/quick_find.py --file-list ... --output-dir outputs/results/run1 &
python scripts/quick_find.py --file-list ... --output-dir outputs/results/run2 &
```

## 🎓 Technical Details

### Checkpoint Format

```json
{
  "results": [
    {"file": "/path/to/file.210", "n_whistles": 45, ...},
    ...
  ],
  "errors": [
    {"file": "/path/to/bad.210", "error": "..."}
  ],
  "last_updated": 1697076123.45
}
```

### Random Sampling

```python
# Line 73 in quick_find.py
file_list = random.sample(all_files, n_files)
```

The sampling is:

- ✅ **Unbiased** - Every file has equal probability
- ✅ **Without replacement** - No duplicates
- ✅ **Reproducible** - Set `random.seed()` if you want same sample

### Checkpoint Frequency

- Saves every **10 files** (configurable in code)
- Balances between:
  - ⚡ Performance (don't save too often)
  - 🛡️ Safety (don't lose too much progress)

## 📈 Expected Performance

| Files  | Time     | Checkpoints | Disk Space |
| ------ | -------- | ----------- | ---------- |
| 100    | ~2 min   | 10          | ~200 KB    |
| 1,000  | ~20 min  | 100         | ~2 MB      |
| 10,000 | ~3 hours | 1,000       | ~20 MB     |

## ❓ FAQ

**Q: What if I run out of disk space during processing?**  
A: The checkpoint will save what's been processed. Add `--resume` to continue.

**Q: Can I change the number of files after starting?**  
A: No, but you can stop and start a new run with different `--n-files`.

**Q: Does it analyze the same files if I don't use --resume?**  
A: No! It does random sampling each time (unless you set `random.seed()`).

**Q: Where is the checkpoint saved?**  
A: `<output-dir>/checkpoint.json` (e.g., `outputs/results/quick_find_results/checkpoint.json`)

**Q: Will the checkpoint interfere with my results?**  
A: No! It's deleted automatically when the run completes successfully.

## 🐬 Try It Now!

```bash
# Quick 3-minute test
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 100

# Medium 20-minute run
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000

# Large overnight run
nohup python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 10000 \
  --resume \
  > overnight.log 2>&1 &
```

Happy analyzing! 🔬🎵🐬
