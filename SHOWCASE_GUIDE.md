# 🐬 Dolphin Acoustic Showcase

## Overview

The **Dolphin Acoustic Showcase** is an interactive web experience that presents the most fascinating dolphin vocalizations discovered through AI-powered analysis.

## Features

### 🎵 Interactive Audio Players

- Switch between raw and denoised audio
- Standard HTML5 audio controls
- Play/pause, volume, scrubbing

### 📊 Beautiful Visualizations

- Spectrograms showing frequency content over time
- Waveforms with whistle detection overlays
- Click to view full-size images in modal

### 📈 Comprehensive Statistics

- Whistle counts and coverage percentages
- Frequency range analysis
- Temporal pattern analysis
- Multi-dolphin interaction detection (overlaps)

### 🌟 Intelligent Highlights

- Automatic badge system for interesting features
- "High Activity" - Files with >70% coverage
- "Rich Communication" - Files with >40 whistles
- "Wide Frequency Range" - >15 kHz frequency span
- "Overlaps" - Multiple dolphins vocalizing simultaneously

### 🎨 Stunning Design

- Dark theme optimized for data visualization
- Gradient backgrounds and animations
- Responsive layout (works on mobile)
- Modal image viewer for detailed inspection

## Usage

### 1. Generate Showcase Data

Run the showcase generator script on your analysis results:

```bash
python scripts/generate_showcase.py \
  --checkpoint outputs/results/large_run/checkpoint.json \
  --top 15 \
  --output-dir site/showcase
```

**Parameters:**

- `--checkpoint`: Path to your analysis results JSON
- `--top`: Number of top files to showcase (default: 15)
- `--output-dir`: Where to save showcase assets (default: site/showcase)

**What it creates:**

```
site/showcase/
├── showcase_data.json          # Main data file for web page
├── audio/                       # Audio files
│   ├── rank_01_*_raw.wav
│   ├── rank_01_*_denoised.wav
│   └── ...
└── images/                      # Visualizations
    ├── rank_01_*_spectrogram.png
    ├── rank_01_*_waveform.png
    └── ...
```

### 2. View the Showcase

Open `site/showcase.html` in a web browser, or deploy it to your web server:

```bash
# Local preview
open site/showcase.html

# Or use Python's HTTP server
cd site
python -m http.server 8000
# Then visit: http://localhost:8000/showcase.html
```

### 3. Deploy to Production

Copy the showcase directory to your web server:

```bash
# Copy to GitHub Pages site directory
cp -r site/showcase/* site/

# Or deploy directly
rsync -av site/showcase/ user@server:/var/www/html/showcase/
```

## How It Works

### Processing Pipeline

1. **Read Results**: Loads top files from checkpoint/results JSON
2. **Audio Processing**:
   - Reads EARS file
   - Applies wavelet denoising
   - Detects whistles
3. **Generate Audio**: Exports both raw and denoised WAV files
4. **Create Visualizations**:
   - Spectrograms with color-coded power
   - Waveforms with whistle overlays
5. **Calculate Statistics**:
   - Whistle metrics (count, duration, frequency)
   - Temporal patterns (gaps, clustering)
   - Quality metrics (SNR, overlaps)
6. **Generate JSON**: Creates `showcase_data.json` for web page

### Web Page Architecture

- **Pure HTML/CSS/JavaScript** - No build step required
- **Responsive Design** - Works on all screen sizes
- **Async Data Loading** - Fetches JSON on page load
- **Modal Viewer** - Click images for full-size view
- **Audio Switching** - Toggle between raw/denoised versions

## Customization

### Changing Colors

Edit `site/showcase.html` CSS variables:

```css
/* Main accent colors */
background: linear-gradient(45deg, #00d4ff, #ff00ff); /* Gradient */
color: #00d4ff; /* Cyan */
color: #ff00ff; /* Magenta */
```

### Adding More Stats

Edit `scripts/generate_showcase.py` in `calculate_statistics()`:

```python
return {
    'whistle_count': len(whistles),
    # Add your custom stat here:
    'your_metric': calculate_your_metric(whistles)
}
```

Then update `site/showcase.html` to display it:

```html
<div class="stat-item">
  <div class="stat-item-value">${stats.your_metric}</div>
  <div class="stat-item-label">Your Metric</div>
</div>
```

### Changing Number of Files

```bash
# Show top 10 instead of 15
python scripts/generate_showcase.py --checkpoint results.json --top 10

# Show top 25
python scripts/generate_showcase.py --checkpoint results.json --top 25
```

## Performance

### Generation Time

- ~15-30 seconds per file
- Mostly CPU-bound (FFT, wavelet transforms)
- Can take 5-10 minutes for 15 files

### File Sizes

- **Audio files**: ~7-8 MB per file (WAV format)
- **Spectrogram images**: ~1 MB per file
- **Waveform images**: ~1 MB per file
- **Total for 15 files**: ~150-200 MB

### Optimization Tips

1. **Reduce Audio Quality** (smaller files):

   ```python
   # In generate_showcase.py, after creating audio:
   import subprocess
   subprocess.run(['ffmpeg', '-i', raw_wav, '-ar', '44100', '-ac', '1',
                   raw_wav.replace('.wav', '_compressed.mp3')])
   ```

2. **Lower Image Resolution**:

   ```python
   # In create_spectrogram_image():
   plt.savefig(output_path, dpi=80)  # Instead of dpi=100
   ```

3. **Show Fewer Files**:
   ```bash
   python scripts/generate_showcase.py --top 10  # Instead of 15
   ```

## Troubleshooting

### "Error loading showcase data"

- Make sure `showcase_data.json` exists in the same directory as `showcase.html`
- Check browser console for CORS errors (use `python -m http.server`)

### Audio won't play

- WAV files must be in the `audio/` subdirectory
- Check browser console for file not found errors
- Try different browser (Chrome/Firefox work best)

### Images not showing

- Images must be in `images/` subdirectory
- Check file paths in `showcase_data.json`
- Verify images were generated successfully

### Generation fails

- Make sure you have enough disk space (~200 MB per 15 files)
- Check that checkpoint JSON is valid
- Verify EARS files still exist at original paths

## Integration with Main Site

The showcase is linked from the main navigation:

```html
<li>
  <a href="showcase.html" class="nav-link nav-special">🐬 Showcase</a>
</li>
```

You can also add a call-to-action section on the homepage:

```html
<section class="showcase-promo">
  <h2>🌟 Explore Real Dolphin Vocalizations</h2>
  <p>Listen to the most fascinating recordings discovered by our AI</p>
  <a href="showcase.html" class="btn-primary">View Showcase →</a>
</section>
```

## Examples

### Sample showcase_data.json structure:

```json
{
  "generated": "2025-10-12T15:30:00",
  "summary": {
    "total_files": 15,
    "total_whistles": 687,
    "total_duration_s": 180.5,
    "avg_whistles_per_file": 45.8,
    "avg_coverage": 82.3,
    "total_overlaps": 23
  },
  "files": [
    {
      "rank": 1,
      "filename": "7175C057.200",
      "score": 52.1,
      "audio_raw": "audio/rank_01_7175C057_raw.wav",
      "audio_denoised": "audio/rank_01_7175C057_denoised.wav",
      "spectrogram": "images/rank_01_7175C057_spectrogram.png",
      "waveform": "images/rank_01_7175C057_waveform.png",
      "stats": {
        "whistle_count": 47,
        "coverage": 92.1,
        "freq_range_khz": 18.3,
        "overlaps": 3
      }
    }
  ]
}
```

## Future Enhancements

Potential additions:

- 🎼 Frequency contour animations
- 📊 Interactive charts (Chart.js/D3.js)
- 🔊 Playback speed control
- 🎯 Whistle-by-whistle navigation
- 📱 Better mobile optimization
- 💾 Download individual files
- 🔗 Share individual recordings
- 📈 Compare multiple recordings side-by-side

## Credits

- **Visualization**: Matplotlib with custom color schemes
- **Audio**: SciPy for WAV file handling
- **Design**: Custom CSS with gradient animations
- **Icons**: Unicode emoji (no external dependencies)

---

**🐬 Ready to showcase your discoveries!**

For questions or issues, see the main project README.
