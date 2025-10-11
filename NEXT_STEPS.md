# Next Steps - Action Plan

## 🎯 Your Batch Processing Framework is Ready!

### ✅ What's Complete

1. **Full batch processing framework** (`dolphain/batch.py`)
2. **100 data files ready** (`data/Buoy210_100300_100399/*.210`)
3. **Example experiments notebook** (`examples/batch_experiments.ipynb`)
4. **Comprehensive documentation** (BATCH_PROCESSING.md)
5. **Tested and validated** (test_batch.py passed)

---

## 🚀 Immediate Next Actions

### Option 1: Run the Example Experiments (Recommended First)

```bash
# Open Jupyter
jupyter notebook examples/batch_experiments.ipynb
```

**What you'll see:**

- 3 complete working experiments
- File discovery and selection examples
- Visualization code ready to use
- Custom experiment template

**Time required:** 10-15 minutes

---

### Option 2: Quick Test Run

```python
import dolphain
import numpy as np

# Find your 100 files
files = dolphain.find_data_files('data', '**/*.210')
print(f"Found {len(files)} files")

# Select a small subset
subset = dolphain.select_random_files(files, n=5, seed=42)

# Define simple pipeline
def quick_stats(filepath):
    data = dolphain.read_ears_file(filepath)
    return {
        'duration': data['duration'],
        'rms': np.sqrt(np.mean(data['data']**2))
    }

# Process
processor = dolphain.BatchProcessor(verbose=True)
collector = processor.process_files(subset, quick_stats)
collector.print_summary()
```

**Time required:** 2-3 minutes

---

### Option 3: Run Full Experiment on All 100 Files

```python
import dolphain
import numpy as np

# Get all files
files = dolphain.find_data_files('data', '**/*.210')
print(f"Processing {len(files)} files...")

# Your analysis pipeline
def my_pipeline(filepath):
    data = dolphain.read_ears_file(filepath)
    acoustic = data['data']

    # Original metrics
    original_rms = np.sqrt(np.mean(acoustic**2))
    original_peak = np.max(np.abs(acoustic))

    # Denoise
    denoised = dolphain.wavelet_denoise(acoustic)
    denoised_rms = np.sqrt(np.mean(denoised**2))

    return {
        'duration': data['duration'],
        'original_rms': original_rms,
        'original_peak': original_peak,
        'denoised_rms': denoised_rms,
        'noise_reduction_pct': (1 - denoised_rms/original_rms) * 100
    }

# Process all files
processor = dolphain.BatchProcessor(verbose=True)
collector = processor.process_files(files, my_pipeline)

# View results
collector.print_summary()

# Export to CSV
import pandas as pd
df = pd.DataFrame(collector.results)
df.to_csv('full_experiment_results.csv', index=False)
print(f"Results saved to full_experiment_results.csv")
```

**Time required:** ~20-30 minutes (100 files × 0.16s each ≈ 16s + analysis time)

---

## 🔬 Research Questions You Can Answer Now

### 1. Data Quality Assessment

**Question:** What's the noise level distribution across all recordings?

```python
def quality_check(filepath):
    data = dolphain.read_ears_file(filepath)
    return {
        'rms': np.sqrt(np.mean(data['data']**2)),
        'snr_estimate': estimate_snr(data['data']),
        'peak': np.max(np.abs(data['data']))
    }
```

### 2. Optimal Wavelet Selection

**Question:** Which wavelet performs best across all files?

```python
def compare_wavelets(filepath):
    data = dolphain.read_ears_file(filepath)
    results = {}
    for wv in ['db4', 'db8', 'db20', 'sym8']:
        denoised = dolphain.wavelet_denoise(data['data'], wavelet=wv)
        results[f'{wv}_snr'] = calculate_snr(data['data'], denoised)
    return results
```

### 3. Temporal Patterns

**Question:** How do acoustic properties vary by time of day/recording?

```python
def temporal_analysis(filepath):
    data = dolphain.read_ears_file(filepath)
    return {
        'hour': data['time_start'].hour,
        'day': data['time_start'].day,
        'rms': np.sqrt(np.mean(data['data']**2)),
        'duration': data['duration']
    }
```

---

## 📊 Visualization Ideas

After collecting results:

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(collector.results)

# Histogram of RMS values
plt.figure(figsize=(10, 6))
df['rms'].hist(bins=30)
plt.xlabel('RMS')
plt.ylabel('Count')
plt.title('Distribution of RMS Across All Files')
plt.savefig('rms_distribution.png')

# Noise reduction effectiveness
plt.figure(figsize=(10, 6))
plt.scatter(df['original_rms'], df['noise_reduction_pct'])
plt.xlabel('Original RMS')
plt.ylabel('Noise Reduction %')
plt.title('Denoising Effectiveness')
plt.savefig('noise_reduction.png')
```

---

## 🎓 Learning Path

### Beginner

1. ✅ Read `README.md` (Quick Start section)
2. ✅ Run `test_batch.py`
3. ✅ Open `examples/batch_experiments.ipynb`
4. ✅ Modify Experiment 1 with your own metrics

### Intermediate

1. ✅ Read `BATCH_PROCESSING.md` fully
2. ✅ Create custom pipeline for your research question
3. ✅ Run on subset of 10-20 files
4. ✅ Analyze results, iterate on pipeline

### Advanced

1. ✅ Process all 100 files with optimized pipeline
2. ✅ Export results to DataFrame
3. ✅ Create publication-quality visualizations
4. ✅ Consider parallel processing for larger datasets

---

## 🛠️ Troubleshooting

### Issue: Import Error

```python
# Solution: Make sure you're in project directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
import dolphain
```

### Issue: File Not Found

```python
# Solution: Check your data directory
files = dolphain.find_data_files('data', '**/*.210')
if not files:
    print("No files found. Check data directory path.")
```

### Issue: Slow Processing

```python
# Solution: Test on subset first
subset = dolphain.select_random_files(files, n=5, seed=42)
# Optimize your pipeline, then scale up
```

---

## 📝 Documentation Quick Reference

| Need                   | Read This                        | Time   |
| ---------------------- | -------------------------------- | ------ |
| Quick start            | README.md                        | 5 min  |
| Batch processing       | BATCH_PROCESSING.md              | 15 min |
| Working examples       | examples/batch_experiments.ipynb | 20 min |
| Implementation details | BATCH_IMPLEMENTATION.md          | 10 min |
| Project overview       | PROJECT_STATUS.md                | 5 min  |

---

## 🎯 Recommended First Step

**I recommend starting here:**

```bash
# 1. Open the batch experiments notebook
jupyter notebook examples/batch_experiments.ipynb

# 2. Run all cells to see examples
# 3. Modify Experiment 1 to test your own metrics
# 4. Scale up to more files when ready
```

This will give you:

- Hands-on experience with the framework
- Working code you can modify
- Visual results to validate
- Template for your own experiments

---

## ✅ You're Ready When...

- [ ] You've run `test_batch.py` successfully
- [ ] You've opened `batch_experiments.ipynb`
- [ ] You understand the pipeline function pattern
- [ ] You know how to find and select files
- [ ] You've seen the result collection work

**Then:** Start defining your research-specific pipelines!

---

## 💡 Pro Tips

1. **Start small:** Test on 3-5 files before running on all 100
2. **Use seeds:** `seed=42` makes results reproducible
3. **Time it:** Use the `timer` context manager to optimize
4. **Save results:** Export to CSV for later analysis
5. **Visualize early:** Plot results as you go to catch issues

---

## 🤔 Questions to Consider

- What metrics matter for your research?
- Which wavelet family works best for your data?
- Are there temporal patterns to explore?
- How much noise reduction is optimal?
- What quality control metrics should you track?

---

## 🚀 You're All Set!

**Everything is working and tested.**

**Your next command:**

```bash
jupyter notebook examples/batch_experiments.ipynb
```

**Or for a quick test:**

```bash
python test_batch.py
```

Good luck with your experiments! 🎉
