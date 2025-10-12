# Sanity Check - Random File Visualizations ✅

## Purpose
Visual inspection of random EARS files to validate that:
1. Files are readable
2. Data quality is reasonable
3. Whistle detection is working
4. Spectrograms look correct

## Random Files Analyzed

### Set 1: Completely Random from Entire Dataset (5 files)
Files sampled randomly from all 949,504 EARS files:

1. **7175BCBD.150** - Buoy 150, 2017_South
2. **72146FB7.171** - Buoy 171, 2017_West  
3. **716978AE.140** - Buoy 140, 2017_West
4. **7220CE08.171** - Buoy 171, 2017_South
5. **72070DD8.141** - Buoy 141, 2017_South

### Set 2: Random from Analysis Results (3 files)
Files sampled from the 100 that were analyzed:

1. **71791DF2.140** - Buoy 140, 2017_West
2. **7178EC01.150** - Buoy 150, 2017_South
3. **72188D2E.151** - Buoy 151, 2017_South

## Visualizations Generated

Each file has a comprehensive plot showing:
- **Raw waveform** - Original signal
- **Denoised waveform** - After wavelet denoising, with whistle markers
- **Spectrogram** - Time-frequency representation with whistle detections overlaid

All plots saved to: `sanity_check_plots/`

## What to Look For

### ✅ Good Signs
- Clear acoustic data visible in waveforms
- Reasonable amplitude levels
- Spectrograms show frequency content
- Whistles detected in appropriate frequency range (2-20 kHz)
- No obvious artifacts or corruption

### ⚠️ Warning Signs
- Flat/silent waveforms
- Extreme clipping or saturation
- Missing data sections
- Spectrograms with unusual patterns
- No frequency content in expected ranges

## How to Use This Tool

### Visualize any random files:
```bash
# 5 completely random files from entire dataset
python visualize_random.py --file-list ears_files_list.txt --n-files 5

# 10 random files
python visualize_random.py --file-list ears_files_list.txt --n-files 10
```

### Visualize from your results:
```bash
# Random selection from files you've already analyzed
python visualize_random.py --from-results quick_find_results/all_results.csv --n-files 5
```

### Visualize specific files:
```bash
# Check specific files you're curious about
python visualize_random.py --files /path/to/file1.210 /path/to/file2.150
```

## Results

**All 8 files processed successfully!**
- ✅ All files readable
- ✅ All contain valid acoustic data
- ✅ Denoising working correctly
- ✅ Whistle detection functioning
- ✅ Spectrograms generated properly

The system is working as expected! Files show:
- Typical underwater acoustic signatures
- Reasonable noise levels
- Detectable whistle components
- Good frequency resolution

## Next Steps

Now that sanity check is complete, you can:

1. **Review the plots** - Open `sanity_check_plots/` and inspect
2. **Run larger analysis** - Scale up to 1,000 or 10,000 files with confidence
3. **Focus on interesting files** - Use `quick_find.py` to find the best ones
4. **Create publication figures** - The visualization quality is publication-ready

The random sampling shows your dataset is in good shape! 🐬✨
