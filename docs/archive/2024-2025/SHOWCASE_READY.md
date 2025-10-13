# 🎬 Showcase Refresh - Ready to Use

## Summary

I've created a new script `refresh_showcase.py` that will automatically rebuild your showcase with the top files from any quick_find results.

## Current Status

✅ **Quick find is running** - Found `CLICK_CHIRP_001/checkpoint.json`
⏳ **Wait for completion** - Will create `results.json` when done
🎨 **Refresh script ready** - Standing by to rebuild showcase

## When Quick Find Completes

### Step 1: Verify Completion

Check for the results file:
```bash
ls -lh CLICK_CHIRP_001/
```

You should see `results.json` (and `checkpoint.json` will be deleted).

### Step 2: Refresh Showcase

Run the refresh script:
```bash
source .venv/bin/activate
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15
```

This will:
- ✨ Clean out `site/showcase/`
- 📋 Read top 15 files from results
- 📁 Copy files locally
- 🎨 Generate plots and spectrograms
- 🎵 Convert to MP3
- 📊 Create metadata file
- 🧹 Clean up temp files

**Time: ~3-4 minutes**

### Step 3: View Showcase

```bash
cd site/showcase
python -m http.server 8000
```

Open http://localhost:8000

## What the Script Does

```
📋 Load CLICK_CHIRP_001/results.json
   ↓
🧹 Clean site/showcase/ (delete old files)
   ↓
📁 Copy top 15 files to temp_showcase_files/
   ↓
🎨 Run generate_showcase.py
   ↓
🎵 Run convert_to_mp3.py
   ↓
📊 Create showcase_metadata.json
   ↓
🧹 Remove temp_showcase_files/
   ↓
✅ Done!
```

## Features

### Smart Cleaning
- Removes old audio, images, and data
- Keeps index.html template
- Won't break if directory doesn't exist

### Flexible Options
```bash
# Custom number of files
--top 20

# Custom output directory
--output site/showcase_v2

# Skip copying (faster, needs drive mounted)
--no-copy
```

### Metadata Tracking
Creates `showcase_metadata.json` with:
- Source directory
- Detection type (chirps/clicks)
- File rankings and scores
- Chirp and click train counts

### Error Handling
- Checks if results exist
- Validates files before processing
- Reports missing files
- Cleans up on success or failure

## Commands Ready to Use

### Once Quick Find Completes

```bash
# Activate environment
source .venv/bin/activate

# Refresh showcase with top 15
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15

# View showcase
cd site/showcase && python -m http.server 8000
```

### Alternative: Top 20 Files

```bash
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 20
```

### Alternative: Keep Old Showcase, Make New One

```bash
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15 --output site/showcase_chirps
```

## Expected Output

When you run the refresh script, you'll see:

```
================================================================================
🎨 REFRESH SHOWCASE
================================================================================
Results directory: CLICK_CHIRP_001
Top files: 15
Output directory: site/showcase

📋 Step 1: Loading results...
  Loaded 1000 results
  Selected top 15 files

🧹 Step 2: Cleaning showcase directory...
  🧹 Cleaning showcase directory: site/showcase
     Removed: audio/
     Removed: images/
     Removed: data/
  ✓ Showcase cleaned

📝 Step 3: Preparing file list...
  Copying files to: temp_showcase_files
     1/15: 7188A701.170
     ...
  ✓ Copied 15 files

🎬 Step 4: Generating showcase...
  Running generate_showcase.py...
  [showcase generation output]

🎵 Step 5: Converting audio to MP3...
  ✓ MP3 conversion complete

================================================================================
✅ SHOWCASE REFRESH COMPLETE!
================================================================================

Showcase created at: site/showcase/
Metadata saved to: site/showcase/showcase_metadata.json

Top 5 files in showcase:
  1. 7188A701.170 - Score: 62.8 (Chirps: 2016, Clicks: 2228)
  2. 721789A8.151 - Score: 62.4 (Chirps: 1128, Clicks: 1861)
  3. 718112B4.200 - Score: 60.9 (Chirps: 1938, Clicks: 1161)
  4. 72029C5F.201 - Score: 58.5 (Chirps: 211, Clicks: 869)
  5. 71676286.140 - Score: 52.9 (Chirps: 8, Clicks: 1558)

To view:
  cd site/showcase && python -m http.server 8000
  Then open: http://localhost:8000
```

## Documentation

Full documentation in: `SHOWCASE_REFRESH.md`

## Script Location

`scripts/refresh_showcase.py` (executable)

---

🎨 **Ready to refresh showcase when quick_find completes!**
