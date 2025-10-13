# 🎨 Showcase Refresh Tool

## Overview

The `refresh_showcase.py` script automatically rebuilds your showcase with the top files from any `quick_find` run results.

## What It Does

1. **Cleans** the showcase directory (removes old files)
2. **Reads** top N files from quick_find results
3. **Copies** files locally (or uses paths directly)
4. **Generates** showcase with plots and spectrograms
5. **Converts** audio to MP3 for web playback
6. **Creates** metadata file documenting the showcase

## Usage

### Basic Usage (Top 15 from CLICK_CHIRP_001)

```bash
source .venv/bin/activate
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15
```

This will:
- Clean out `site/showcase/`
- Take the top 15 files from `CLICK_CHIRP_001/results.json`
- Copy them to `temp_showcase_files/`
- Generate full showcase with plots
- Convert to MP3
- Clean up temp files

### Custom Number of Files

```bash
# Top 20 files
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 20

# Top 10 files (faster)
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 10
```

### Custom Output Directory

```bash
# Create alternate showcase
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15 --output site/showcase_v2
```

### Fast Mode (No Copy)

If the external drive is mounted and you want to skip the copy step:

```bash
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15 --no-copy
```

⚠️ **Warning**: Files must remain accessible at their original paths!

## Output

### Files Created

In the showcase directory (`site/showcase/` by default):

```
site/showcase/
├── index.html           # Main showcase page
├── audio/               # WAV and MP3 files
├── images/              # PNG spectrograms and plots
├── data/                # JSON data files
└── showcase_metadata.json  # Metadata about this showcase
```

### Metadata File

The `showcase_metadata.json` file contains:
- Source results directory
- Number of files analyzed
- Detection type (chirps, click_trains)
- List of files with ranks and scores

Example:
```json
{
  "source": "CLICK_CHIRP_001",
  "top_n": 15,
  "detection_type": ["chirps", "click_trains"],
  "files": [
    {
      "rank": 1,
      "filename": "7188A701.170",
      "score": 62.8,
      "n_chirps": 2016,
      "n_click_trains": 12,
      "total_clicks": 2228
    },
    ...
  ]
}
```

## Workflow

### After Quick Find Completes

1. **Wait for quick_find to finish** (check for `results.json`)
2. **Run refresh_showcase**:
   ```bash
   python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15
   ```
3. **View the showcase**:
   ```bash
   cd site/showcase && python -m http.server 8000
   ```
   Open http://localhost:8000

### Multiple Showcases

You can create multiple showcases from different runs:

```bash
# Chirp/Click showcase
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15 --output site/showcase_chirps

# Future whistle showcase (if you run whistle detection)
python scripts/refresh_showcase.py --results-dir WHISTLE_001 --top 15 --output site/showcase_whistles
```

## Timing

For top 15 files:
- Copy files: ~5-10 seconds
- Generate showcase: ~2-3 minutes
- MP3 conversion: ~30 seconds
- **Total: ~3-4 minutes**

For top 20 files: ~4-5 minutes

## Troubleshooting

### "Results file not found"
- Quick_find is still running - wait for it to complete
- Or you specified the wrong directory name

### "File not found" warnings
- Files have been moved or deleted
- External drive not mounted
- Use `--no-copy` if files are on external drive

### Showcase generation fails
- Check that `generate_showcase.py` exists
- Make sure virtual environment is activated
- Check disk space

### MP3 conversion warnings
- Usually okay - WAV files will work in showcase
- Check if `ffmpeg` is installed: `which ffmpeg`

## Advanced Usage

### Chain Multiple Operations

Generate showcase immediately after quick_find:

```bash
# Run quick_find
python scripts/quick_find.py --file-list outputs/ears_files_list.txt --n-files 1000 --output-dir CLICK_CHIRP_001

# When complete, refresh showcase
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15

# Start web server
cd site/showcase && python -m http.server 8000
```

### Background Processing

Run showcase generation in background:

```bash
nohup python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 20 > showcase_log.txt 2>&1 &
```

Monitor progress:
```bash
tail -f showcase_log.txt
```

## Commands Quick Reference

```bash
# Activate environment
source .venv/bin/activate

# Refresh showcase (top 15)
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15

# View showcase
cd site/showcase && python -m http.server 8000
# Open: http://localhost:8000

# Check metadata
cat site/showcase/showcase_metadata.json | python -m json.tool
```

## Notes

- The script is **destructive** - it deletes existing showcase files
- Original EARS files and results are never modified
- Temp files are automatically cleaned up
- Safe to run multiple times (idempotent)

🎨 Happy showcasing!
