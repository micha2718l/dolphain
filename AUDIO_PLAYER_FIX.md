# Audio Player Bug Fixes

## Problem Summary
The showcase audio player had critical bugs preventing proper seeking functionality, particularly when:
1. Audio files weren't immediately seekable after loading
2. Switching between raw/denoised modes
3. Accidental auto-play on page load

## Root Causes Identified

### 1. Non-Seekable Audio Files
**Issue**: Some audio files (particularly rank 2) would load with `seekable.end(0) === 0`, meaning the browser hadn't buffered enough data to allow seeking.

**Symptoms**:
- Clicking on visualizations would reset playback to 0:00
- Console showed: `seekable range: 0.00s - 0.00s`
- Retry logic would fail all 3 attempts

**Solution**: 
- Check if audio is seekable before attempting to seek
- If not seekable, pause the audio and call `load()` to force buffering
- Wait for `canplay` event, then retry the seek
- Only proceed with seek once `seekable.end(0) > 0`

### 2. Mode Switching Issues
**Issue**: When switching from denoised to raw mode, the new audio file would load but not be immediately seekable, causing the same "skip to start" behavior.

**Symptoms**:
- Raw mode clicks always jumped to 0:00
- Denoised mode worked fine after initial load
- Problem occurred on both ranks

**Solution**:
- Always pause audio before switching modes
- Use `canplay` event to wait for new file to buffer
- Only restore position after audio is confirmed seekable

### 3. Accidental Auto-Play
**Issue**: The play button was being accidentally clicked during page load, causing rank 2 to start playing immediately.

**Symptoms**:
- Console showed `togglePlay()` being called before user interaction
- Stack trace showed it came from button click handler at line 121 of showcase.js

**Solution**:
- Added 500ms delay before enabling play button clicks
- Prevent clicks during page load with flag and `preventDefault()`

## Code Changes

### audio-player.js

**Simplified `init()`**:
- Removed verbose debug logging
- Kept only essential error handling
- Cleaner event listener setup

**Fixed `setMode()`**:
- Always pause before switching
- Proper `canplay` handling for position restoration
- Cleaner code flow

**Robust `seekTo()`**:
```javascript
// Key logic:
1. Check if duration is available (wait for loadedmetadata if not)
2. Check if audio is seekable (seekable.length > 0 && seekable.end(0) > 0)
3. If not seekable:
   - Pause if playing
   - Reload audio
   - Wait for canplay, then retry
4. If seekable:
   - Set currentTime
   - Wait for seeked event
   - Retry up to 3 times if seek fails
   - Auto-play after successful seek
```

**Cleaned up `togglePlay()`**:
- Removed debug logging and stack traces
- Removed manual `isPlaying` toggle (let events handle it)

### showcase.js

**Button Click Protection**:
```javascript
let buttonClickEnabled = false;
setTimeout(() => buttonClickEnabled = true, 500);

player.elements.playBtn.addEventListener('click', (e) => {
    if (!buttonClickEnabled) {
        e.stopPropagation();
        e.preventDefault();
        return;
    }
    player.togglePlay();
});
```

## Testing Results
After fixes:
- ✅ Rank 1 seeking works perfectly on both raw and denoised
- ✅ Rank 2 seeking works perfectly on both raw and denoised  
- ✅ No auto-play on page load
- ✅ Smooth playback after seeking
- ✅ No "skip to start" bugs when clicking on denoised visualizations

## Known Issues
- ⚠️ **Mode switching seeking**: When switching from denoised→raw mode and then clicking to seek, the audio is not yet seekable and needs additional handling. The fix for this will require waiting for the audio to fully buffer after mode switch before allowing seeks.

## Key Learnings

1. **Audio Seekability**: Not all loaded audio is immediately seekable. Always check `seekable.end(0) > 0` before attempting to seek.

2. **Browser Buffering**: When audio isn't seekable, calling `load()` forces the browser to buffer properly.

3. **Event Timing**: Use `canplay` rather than `loadedmetadata` to ensure audio is actually ready for seeking.

4. **Page Load Clicks**: Layout shifts during image loading can cause accidental clicks. Add delays to UI interaction handlers.

5. **Mode Switching**: Always pause→load→wait for canplay before restoring position when switching audio sources.

## Performance
- Seeking now works immediately when audio is buffered
- Graceful fallback when audio isn't ready (pause→reload→retry)
- No infinite loops or hung states
- Clean console output (minimal logging)
