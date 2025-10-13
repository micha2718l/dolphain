# Showcase Quick Reference

## 🎯 Quick Start

```bash
# Start local server
cd /Users/mjhaas/code/dolphain/site
python3 -m http.server 8000

# Open in browser
open http://localhost:8000/showcase.html
```

## 📁 File Structure

```
site/
├── showcase.html                 # Main page (16 lines)
├── css/showcase.css              # Styling (150 lines)
├── js/
│   ├── audio-player.js          # AudioPlayer class (194 lines)
│   └── showcase.js              # UI logic (148 lines)
└── showcase/
    ├── showcase_data.json       # File metadata
    ├── audio/                   # WAV files
    ├── spectrograms/            # PNG images
    └── waveforms/               # PNG images
```

## 🔧 Making Changes

### Add More Files
```bash
# When external drive is connected
cd /Users/mjhaas/code/dolphain

# Generate showcase from top results
/Users/mjhaas/code/dolphain/.venv/bin/python \
  scripts/generate_showcase.py \
  --checkpoint quick_find_results/results.json \
  --top 10 \
  --output-dir site/showcase
```

### Modify Styling
Edit `site/css/showcase.css`:
- Colors: Search for `#00d4ff` (cyan accent)
- Dark theme: `#0a1628` → `#1a2f4a` gradient
- Card width: `.file-card { max-width: 1200px; }`
- Visualization height: `.spec-container { height: 180px; }`

### Modify Player Behavior
Edit `site/js/audio-player.js`:
- Seek retry count: Change `> 3` in line ~147
- Button delay: Change `500` ms in showcase.js line ~121
- Autoplay after seek: Change `if (!this.isPlaying)` in line ~166

### Add Features
Edit `site/js/showcase.js`:
- Add event listeners in the main fetch block (lines 40-140)
- Modify card HTML generation (lines 60-110)
- Add new UI elements to showcase.html

## 🐛 Debugging

### Audio Not Playing
1. Check console for errors
2. Verify audio file exists: `ls site/showcase/audio/`
3. Check audio format: `file site/showcase/audio/rank_01_*.wav`
4. Test audio directly: `afplay site/showcase/audio/rank_01_*.wav`

### Seeking Not Working
1. Check if audio is seekable: Look for "seekable range" in console
2. Wait for audio to load fully (green canplay event)
3. Try pausing and reloading: Click pause, then seek
4. Check browser console for errors

### Mode Switching Issues
1. Known issue: Seeking after mode switch may not work
2. Workaround: Wait 1-2 seconds after switching before seeking
3. Better fix: Add buffering wait in audio-player.js setMode()

### Images Not Loading
1. Check image paths in showcase_data.json
2. Verify images exist: `ls site/showcase/spectrograms/`
3. Check image format: `file site/showcase/spectrograms/*.png`
4. Clear browser cache: Cmd+Shift+R (Mac)

## 📊 Data Format

### showcase_data.json Structure
```json
{
  "generated": "timestamp",
  "summary": {
    "total_files": 2,
    "total_whistles": 123,
    "total_duration_s": 42.7
  },
  "files": [
    {
      "rank": 1,
      "filename": "71664B69.140",
      "audio_raw": "audio/rank_01_71664B69_raw.wav",
      "audio_denoised": "audio/rank_01_71664B69.wav",
      "spectrogram_raw": "spectrograms/rank_01_71664B69_raw.png",
      "spectrogram_denoised": "spectrograms/rank_01_71664B69.png",
      "waveform_raw": "waveforms/rank_01_71664B69_raw.png",
      "waveform_denoised": "waveforms/rank_01_71664B69.png",
      "stats": {
        "whistle_count": 45,
        "duration": 21.33,
        "coverage": 95.2
      },
      "metadata": {
        "time_start": "2017-08-15T12:34:56",
        "duration": 21.33
      },
      "score": 85.0
    }
  ]
}
```

## 🎨 Customization

### Change Theme Colors
```css
/* In css/showcase.css */

/* Background gradient */
body {
    background: linear-gradient(135deg, #YOUR_COLOR1, #YOUR_COLOR2);
}

/* Accent color (timeline, hover, etc) */
.playback-line { background: #YOUR_ACCENT; }
.timeline { background: #YOUR_ACCENT; }
.hover-line { border-left: 2px solid #YOUR_ACCENT; }
```

### Add Keyboard Shortcuts
```javascript
// In js/showcase.js, add to main block:
document.addEventListener('keydown', (e) => {
    if (e.key === ' ') {
        e.preventDefault();
        // Get active player and toggle
        const activeCard = document.querySelector('.file-card');
        const rank = activeCard.id.split('-')[1];
        players[rank].togglePlay();
    }
});
```

### Add Download Button
```javascript
// In js/showcase.js card generation:
const downloadBtn = document.createElement('a');
downloadBtn.href = `showcase/${file.audio_denoised}`;
downloadBtn.download = file.filename;
downloadBtn.textContent = '⬇️ Download';
downloadBtn.className = 'download-btn';
audioControls.appendChild(downloadBtn);
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] Page loads without errors
- [ ] Both cards display correctly
- [ ] Spectrograms and waveforms show
- [ ] Clicking on visualizations seeks and plays
- [ ] Play/pause button works
- [ ] Timeline scrubber works
- [ ] Current time updates during playback
- [ ] No auto-play on page load
- [ ] Denoised tab is active by default
- [ ] Hover line shows on mouse over

### Browser Testing
Test in multiple browsers:
- [ ] Chrome/Brave (Chromium-based)
- [ ] Safari (WebKit)
- [ ] Firefox (Gecko)

### Performance Testing
Check browser console for:
- [ ] No errors on page load
- [ ] Audio loads in < 2 seconds
- [ ] Images load in < 1 second
- [ ] Smooth animations (60fps)
- [ ] No memory leaks (reload 10x, check memory)

## 📚 References

- Main docs: `AUDIO_PLAYER_FIX.md`, `SHOWCASE_CLEANUP.md`
- Generation script: `scripts/generate_showcase.py`
- Test data: `site/showcase/showcase_data.json`
- MDN Audio API: https://developer.mozilla.org/en-US/docs/Web/API/HTMLAudioElement

## 🆘 Common Issues

### "File not found" during generation
- External drive not mounted
- Check path in results.json matches actual files
- Run with `--top 2` to test with fewer files

### Showcase shows 0 files
- Check showcase_data.json exists and has "files" array
- Verify audio/image files exist in subdirectories
- Check browser console for fetch errors

### Audio plays but doesn't seek
- Wait for audio to fully load (canplay event)
- Check seekable range in console (should be > 0)
- Try pausing before seeking

### Mode switching breaks playback
- Known issue - fix in progress
- Workaround: Pause, switch mode, wait 1s, then seek
