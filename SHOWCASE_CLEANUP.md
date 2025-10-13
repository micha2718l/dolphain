# Showcase Cleanup - October 12, 2025

## What Was Done

### 1. Code Cleanup

Cleaned up and modularized the showcase code:

**Before**: Monolithic 500+ line HTML file with embedded CSS and JavaScript
**After**: Clean modular structure:

- `showcase.html` - 16 lines, clean HTML structure
- `css/showcase.css` - 150 lines, all styling
- `js/audio-player.js` - 194 lines, AudioPlayer class
- `js/showcase.js` - 148 lines, UI and initialization

### 2. Audio Player Fixes

Fixed critical bugs in audio playback:

- ✅ Non-seekable audio handling (files not immediately bufferable)
- ✅ Accidental auto-play on page load (500ms click delay)
- ✅ "Skip to start" bug when clicking visualizations
- ✅ Proper pause/resume state management
- ✅ Clean error handling without verbose logging

### 3. File Organization

```
site/
├── showcase.html              # Main showcase (clean v3)
├── showcase_v3.html          # Keep as reference
├── archive/
│   └── showcase_v2.html      # Archived old version
├── css/
│   └── showcase.css          # All styling
├── js/
│   ├── audio-player.js       # Audio playback logic
│   └── showcase.js           # UI and initialization
└── showcase/
    ├── showcase_data.json    # Data for 2 test files
    ├── audio/                # WAV files (raw + denoised)
    ├── spectrograms/         # Spectrogram images
    └── waveforms/            # Waveform images
```

### 4. Documentation

Created comprehensive docs:

- `AUDIO_PLAYER_FIX.md` - Detailed breakdown of bugs and fixes
- `SHOWCASE_CLEANUP.md` - This file, overview of cleanup

## Current State

### Working Features

- 🎵 Audio playback (play/pause)
- 🎯 Seeking on spectrograms and waveforms
- ⏱️ Timeline scrubber
- 📊 Synchronized playback line across visualizations
- 🎨 Beautiful dark theme with cyan accents
- 💾 2 showcase files (ranks 1-2) with full data

### Known Issues

- ⚠️ **Mode switching**: Seeking after switching from denoised→raw doesn't work reliably (audio not yet bufferable)
- 📁 **Limited files**: Only 2 files in showcase (test data), need to regenerate with more when external drive is available

### Performance

- Showcase generation: ~3.6s per file (26x improvement from original 95s)
- Page load: Fast, smooth
- Audio loading: Instant for denoised, delayed for non-seekable files
- Image rendering: Fast with imshow optimization

## Technical Improvements

### Code Quality

1. **Separation of Concerns**

   - HTML: Structure only
   - CSS: All styling
   - JS: Split into logical modules (player vs UI)

2. **Class-Based Architecture**

   - `AudioPlayer` class encapsulates all playback logic
   - Clean public API: `init()`, `setMode()`, `seekTo()`, `togglePlay()`
   - Private methods for event handling

3. **Event-Driven Design**

   - Proper use of audio element events (canplay, seeked, loadedmetadata)
   - No polling or timeouts for state checks
   - Clean event listener cleanup with `{ once: true }`

4. **Error Handling**
   - Graceful fallback for non-seekable audio
   - Console errors only for actual problems
   - Silent catch for expected autoplay blocks

### Performance Optimizations

1. **Image Generation** (generate_showcase.py)

   - `imshow` instead of `pcolormesh` (26x faster)
   - `axis('off')` for clean images
   - Agg backend for headless rendering

2. **Audio Loading**

   - `preload='metadata'` for fast initial load
   - Lazy buffering with `load()` on demand
   - Seekable range checking before seeks

3. **UI Responsiveness**
   - 500ms button delay prevents accidental clicks
   - Smooth hover effects with CSS transitions
   - No blocking operations in main thread

## Next Steps

### High Priority

1. **Fix mode switching seeking** - Add proper buffering wait after mode change
2. **Regenerate showcase** - Create full gallery with 10-20 top files when drive available
3. **Test on other browsers** - Verify audio element behavior consistency

### Medium Priority

1. **Add keyboard shortcuts** - Space for play/pause, arrow keys for seeking
2. **Add download buttons** - Let users download interesting audio files
3. **Improve mobile experience** - Touch-friendly controls, responsive layout

### Low Priority

1. **Add zoom on spectrograms** - Click to zoom in on frequency ranges
2. **Add playback speed control** - 0.5x, 0.75x, 1x, 1.5x, 2x
3. **Add comparison mode** - Play two files side-by-side

## Lessons Learned

### Audio Element Gotchas

1. **Not all loaded audio is seekable** - Must check `seekable.end(0) > 0`
2. **Mode switching resets state** - Changing `src` makes audio non-seekable temporarily
3. **Browser differences** - Safari/Chrome handle buffering differently
4. **Autoplay policies** - Modern browsers block autoplay, need user interaction

### Development Best Practices

1. **Start modular** - Don't let files grow to 500+ lines
2. **Add logging strategically** - Too much logging hides the signal
3. **Use browser events** - Don't poll or guess state
4. **Test edge cases** - Non-seekable audio, mode switching, rapid clicks

### Performance Tips

1. **Matplotlib Agg backend** - Essential for server-side rendering
2. **imshow vs pcolormesh** - Huge performance difference for images
3. **Event listeners with { once: true }** - Prevent memory leaks
4. **CSS over JS** - Use CSS transitions for smooth UI

## Files Modified

### New Files

- `site/showcase.html` - Main showcase page
- `site/css/showcase.css` - Showcase styling
- `site/js/audio-player.js` - Audio player class
- `site/js/showcase.js` - Showcase UI logic
- `AUDIO_PLAYER_FIX.md` - Bug fix documentation
- `SHOWCASE_CLEANUP.md` - This file

### Modified Files

- None (started fresh with v3)

### Archived Files

- `site/archive/showcase_v2.html` - Old monolithic version

## Validation

To test the cleaned-up showcase:

```bash
cd /Users/mjhaas/code/dolphain/site
python3 -m http.server 8000
# Open http://localhost:8000/showcase.html
```

Expected behavior:

1. Page loads with 2 cards (ranks 1-2)
2. Clicking on spectrograms/waveforms seeks and plays
3. Play button works (▶/⏸)
4. Timeline scrubber works
5. Denoised tab is active by default
6. No "skip to start" bugs on denoised mode
7. No auto-play on page load

## References

- Audio element API: https://developer.mozilla.org/en-US/docs/Web/API/HTMLAudioElement
- TimeRanges (seekable): https://developer.mozilla.org/en-US/docs/Web/API/TimeRanges
- Autoplay policy: https://developer.chrome.com/blog/autoplay/
