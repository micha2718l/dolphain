# 🚀 Quick Commands for Showcase Generation

## Two-Step Process (For Disconnected Drive)

### Step 1: Copy Files (When Drive is Connected)
```bash
# Copy top 25 files from your analysis to local temp directory
python scripts/copy_top_files.py \
  --checkpoint outputs/results/large_runENHANCED/checkpoint.json \
  --top 25 \
  --output-dir temp_showcase_files
```

**What this does:**
- Reads your analysis results
- Copies the top 25 EARS files to `temp_showcase_files/`
- Creates a manifest.json for tracking
- Shows you which files were copied successfully

**Output:** `temp_showcase_files/` with .200/.201 files

---

### Step 2: Generate Showcase (Anytime, Drive Not Needed)
```bash
# Generate showcase from local files
python scripts/generate_showcase_local.py \
  --input-dir temp_showcase_files \
  --top 25 \
  --output-dir site/showcase
```

**What this does:**
- Processes local EARS files
- Creates spectrograms and waveforms
- Exports raw and denoised audio
- Generates showcase_data.json

**Output:** `site/showcase/` ready to deploy

---

## One-Step Process (Drive Connected)

If your external drive is connected, use the original method:

```bash
python scripts/generate_showcase.py \
  --checkpoint outputs/results/large_runENHANCED/checkpoint.json \
  --top 25 \
  --output-dir site/showcase
```

---

## Quick Reference

### Copy different numbers of files:
```bash
# Top 10
python scripts/copy_top_files.py --checkpoint results.json --top 10

# Top 50
python scripts/copy_top_files.py --checkpoint results.json --top 50
```

### Use different directories:
```bash
# Custom temp location
python scripts/copy_top_files.py \
  --checkpoint results.json \
  --output-dir /path/to/temp

# Custom showcase output
python scripts/generate_showcase_local.py \
  --input-dir /path/to/temp \
  --output-dir site/my_showcase
```

### View the showcase:
```bash
# Open in browser
open site/showcase.html

# Or use local server
cd site
python -m http.server 8000
# Visit: http://localhost:8000/showcase.html
```

---

## Typical Workflow

1. **Run large analysis** (takes hours):
   ```bash
   python scripts/quick_find.py --n-files 10000
   ```

2. **When done, copy top files** (drive connected):
   ```bash
   python scripts/copy_top_files.py --checkpoint checkpoint.json --top 25
   ```

3. **Disconnect drive if needed**

4. **Generate showcase** (can do offline):
   ```bash
   python scripts/generate_showcase_local.py --input-dir temp_showcase_files
   ```

5. **View results**:
   ```bash
   open site/showcase.html
   ```

6. **Deploy** (optional):
   ```bash
   git add site/showcase/
   git commit -m "Update showcase with top 25 files"
   git push
   ```

---

## File Sizes

- Each EARS file: ~500 KB
- Each raw WAV: ~16 MB
- Each denoised WAV: ~16 MB  
- Each spectrogram: ~200-300 KB
- Each waveform: ~70-80 KB

**Total for 25 files: ~800 MB**

---

## Troubleshooting

### "No such file or directory"
- External drive not connected
- Use two-step process instead

### "No EARS files found"
- Check that files have .200, .201, etc. extensions
- Verify input directory path

### Files hanging during processing
- Normal for files with many whistles (can take 2-3 minutes each)
- Script shows progress for each step

---

## Pro Tips

💡 **Copy files overnight** - Do Step 1 when you start a new analysis, so files are ready

💡 **Multiple showcases** - Create themed showcases (high activity, overlaps, etc.)

💡 **Version control** - Keep temp_showcase_files/ in .gitignore (large files)

💡 **Backup** - Save temp_showcase_files/ to cloud storage for safekeeping
