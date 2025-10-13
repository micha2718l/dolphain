# 🤖 LLM Session Onboarding - Dolphain Project

**Purpose:** Quick briefing for new LLM sessions to understand this project

**Last Updated:** October 12, 2025

---

## 📋 Quick Brief

**Project:** Dolphain - Dolphin acoustic analysis toolkit  
**Language:** Python  
**Type:** Research tool + interactive web showcase  
**Status:** Production ready, actively developed  
**User:** Michael Haas (micha2718l)

---

## 🎯 What This Project Does

Analyzes underwater acoustic recordings (EARS files) to detect dolphin vocalizations:

1. **Detection:** Finds chirps (frequency sweeps) and click trains (echolocation)
2. **Analysis:** Scores files by "interestingness" (0-100 scale)
3. **Showcase:** Web gallery with interactive audio player and visualizations

**Key Innovation:** Conservative detection algorithms that minimize false positives

---

## 📁 Essential Files to Read First

### For Understanding the Project

1. **`START_HERE.md`** - Quick status, what's working now (2 min)
2. **`HANDOFF_NOTES.md`** - Complete technical overview (10 min)
3. **`README.md`** - API documentation and examples

### For Current Status

- **`CURRENT_STATUS.md`** - Latest state and next steps
- **`FINAL_STATUS_OCT2025.md`** - Comprehensive Oct 2025 summary
- **`DOC_INDEX.md`** - Full documentation navigation

### For Specific Tasks

- **Showcase work:** `SHOWCASE_QUICK_REF.md`
- **Detection algorithms:** `CHIRP_CLICK_DETECTION.md`
- **Audio player:** `AUDIO_PLAYER_FIX.md`

---

## 🏗️ Architecture Overview

```
dolphain/
├── dolphain/              # Python library (core algorithms)
│   ├── io.py              # Read EARS files, WAV export
│   ├── signal.py          # Wavelet denoising, detection
│   ├── plotting.py        # Spectrogram/waveform visualization
│   └── batch.py           # Parallel processing
│
├── scripts/               # Command-line tools
│   ├── quick_find.py      # Find interesting files (chirp/click detection)
│   ├── generate_showcase.py  # Create web showcase
│   └── ears_to_wav.py     # Convert EARS → WAV
│
├── site/                  # Interactive web showcase
│   ├── showcase.html      # Main page (16 lines - modular)
│   ├── css/showcase.css   # Styling (150 lines)
│   ├── js/
│   │   ├── audio-player.js  # AudioPlayer class (194 lines)
│   │   └── showcase.js      # UI logic (148 lines)
│   └── showcase/          # Generated assets
│       ├── showcase_data.json
│       ├── audio/         # WAV files (raw + denoised)
│       └── images/        # PNG visualizations
│
└── docs/                  # Documentation
    └── archive/           # Historical docs
```

---

## 🎨 Current Showcase Features

**What Works:**

- ✅ Interactive audio player with click-to-seek
- ✅ Drag scrubbing on waveforms (desktop + mobile)
- ✅ Raw/denoised mode switching (preserves position)
- ✅ Synchronized waveform + spectrogram highlighting
- ✅ Professional dark theme UI
- ✅ Keyboard shortcuts (Space = play/pause)
- ✅ Fast generation (3.6s per file, 26x improvement)

**Known Issue:**

- ⚠️ After mode switch, seeking requires 1-2 sec wait (audio becomes non-seekable temporarily)

---

## 🐬 Detection Algorithms

### Chirp Detection (Conservative)

Detects frequency sweeps in spectrograms:

- Min duration: 0.3s (longer = more selective)
- Min frequency sweep: 3 kHz
- Only top 3 strongest peaks per time window
- Rejects erratic jumps (smooth sweeps only)

### Click Train Detection (Conservative)

Detects dolphin echolocation:

- Frequency range: 20-150 kHz (high-frequency only)
- Min clicks per train: 10
- Max inter-click interval: 50ms
- Sharp peaks only (rejects wide noise bumps)

### Scoring (0-100 scale)

- 40 points: Chirp activity (quantity, sweep quality, diversity)
- 40 points: Click train activity (quantity, regularity, rate)
- 20 points: Signal quality (SNR, clarity)

---

## 🚀 Common Commands

### View Showcase Locally

```bash
cd /Users/mjhaas/code/dolphain/site
python3 -m http.server 8000
# Open: http://localhost:8000/showcase.html
```

### Analyze Files (Find Interesting Ones)

```bash
source .venv/bin/activate
python scripts/quick_find.py \
  --file-list ears_files_list.txt \
  --n-files 100 \
  --output-dir quick_find_results
```

### Generate Showcase

```bash
python scripts/generate_showcase.py \
  --checkpoint quick_find_results/results.json \
  --top 10 \
  --output-dir site/showcase
```

### Convert Single File

```bash
python scripts/ears_to_wav.py /path/to/file.ears --plot
```

---

## 📊 Performance Metrics

- **Analysis:** ~1-2 files/second (depends on file size)
- **Generation:** 3.6s per showcase file
- **File size:** ~8 MB per EARS file (30-second recordings)
- **Showcase assets:** ~1 MB per file (4 images + 2 audio)

---

## 🎯 User's Priorities & Preferences

### What User Values

1. **Clean code:** Modular, well-commented, under 300 lines per file
2. **Documentation:** Keep docs updated, create comprehensive guides
3. **Git hygiene:** Good commit messages, logical commits, clean history
4. **Conservative detection:** Fewer false positives > more detections
5. **Performance:** Fast enough for real-time workflow

### Working Style

- User makes manual edits (respects this, don't auto-revert)
- Prefers comprehensive docs over brief comments
- Likes seeing command outputs and examples
- Appreciates detailed commit messages
- Values "show, don't just tell" approach

### Communication Style

- Be direct and technical
- Show examples and command outputs
- Explain reasoning for decisions
- Provide complete solutions, not just snippets
- Use clear status indicators (✅ ❌ ⚠️)

---

## 🛠️ Best Practices for This Project

### Code Changes

1. **Read context first** - Check existing code before editing
2. **Keep files modular** - No monolithic files (aim for <300 lines)
3. **Use class-based design** - AudioPlayer, Showcase manager classes
4. **Event-driven** - Prefer event listeners over polling
5. **Document decisions** - Create markdown docs for major changes

### Git Workflow

1. **Check status first** - Always check what's uncommitted
2. **Group related changes** - Logical commits, not "misc fixes"
3. **Write good messages** - Explain what AND why
4. **Update docs in same commit** - Keep code & docs in sync
5. **Check .gitignore** - Don't commit test data or large files

### Documentation

1. **Update START_HERE.md** - Keep current status accurate
2. **Create guides for major features** - Like AUDIO_PLAYER_FIX.md
3. **Use DOC_INDEX.md** - Add new docs to the index
4. **Archive old docs** - Don't delete, move to docs/archive/
5. **Include examples** - Commands, code snippets, outputs

### Testing

1. **Test locally first** - View showcase before committing
2. **Check cross-browser** - Safari, Firefox, Chrome
3. **Test edge cases** - Empty files, errors, mode switching
4. **Validate performance** - Check generation times
5. **Document known issues** - Don't hide problems

---

## 📦 Data & Files

### Source Data

- **Location:** External drive (not always mounted)
- **Format:** EARS files (proprietary binary format)
- **Size:** 949,504 files total (~8 MB each)
- **Note:** Don't commit EARS files to git (too large)

### Test Data

- **Ignored by git:** temp*showcase_files/, test*_, CLICK*CHIRP*_
- **Can regenerate:** All test results are from running scripts
- **Size matters:** Test dirs can be 300+ MB, keep out of git

### Generated Assets

- **Showcase:** site/showcase/ (HTML, audio, images)
- **Results:** quick_find_results/ (JSON, CSV)
- **Outputs:** outputs/ (various analysis results)

---

## 🔧 Current Development State

### Just Completed (Oct 12, 2025)

- ✅ Modernized showcase with modular architecture
- ✅ Comprehensive documentation cleanup (17 docs archived)
- ✅ New chirp/click detection algorithms
- ✅ Helper scripts for workflow automation
- ✅ Git cleanup (proper .gitignore, clean history)

### Ready for Next Phase

- Fix mode switching seeking delay
- Regenerate showcase with 10-20 files (need drive)
- Cross-browser testing
- Consider keyboard shortcuts enhancement

### Not Urgent

- Playback speed control
- Download buttons
- Mobile optimization
- Spectrogram zoom

---

## ⚠️ Known Issues

1. **Mode switching seeking** (documented in AUDIO_PLAYER_FIX.md)

   - After switching raw↔denoised, audio is temporarily non-seekable
   - Workaround: Wait 1-2 seconds after mode switch
   - Fix: Add proper buffering check in audio-player.js

2. **Limited showcase files** (only 2 test files currently)

   - Need external drive mounted to regenerate with more files
   - Not a code issue, just data availability

3. **No mobile optimization yet**
   - Works on mobile but not optimized
   - Consider touch gestures, layout improvements

---

## 🎓 Project-Specific Knowledge

### EARS File Format

- Proprietary binary format from underwater recorders
- Contains: timestamp, GPS, temperature, audio data (250 kHz)
- Read with: `dolphain.read_ears_file(path)`
- Duration: Usually 30 seconds

### Wavelet Denoising

- Uses PyWavelets library (db8 wavelet)
- Removes low-amplitude noise while preserving signals
- Essential preprocessing step before detection
- Trade-off: Over-denoising removes faint signals

### Interestingness Score

- Not just whistle count - multi-factor scoring
- Designed to find "interesting" recordings for researchers
- Conservative: Better to miss than have false positives
- Tuned through empirical testing on real data

### Web Showcase Design

- Must work without server (static files only)
- No database, no backend - just JSON data
- Supports offline viewing
- GitHub Pages compatible

---

## 💡 Quick Tips

1. **Check CURRENT_STATUS.md first** - Always know latest state
2. **Use DOC_INDEX.md** - Find relevant docs quickly
3. **Test locally** - python3 -m http.server 8000
4. **Check git status** - Before and after changes
5. **Read HANDOFF_NOTES.md** - Complete technical context
6. **Follow existing patterns** - Look at current code style
7. **Document as you go** - Update docs in same commit
8. **Ask about data location** - External drive may not be mounted

---

## 🚨 Don't Do This

❌ Commit large EARS files (8 MB each)  
❌ Commit test data directories (use .gitignore)  
❌ Make 500+ line monolithic files  
❌ Break existing working features  
❌ Skip documentation updates  
❌ Auto-revert user's manual edits without asking  
❌ Assume drive is mounted (check first)  
❌ Ignore .gitignore patterns

---

## ✅ Do This

✅ Read START_HERE.md and CURRENT_STATUS.md first  
✅ Check git status before making changes  
✅ Keep files modular and well-documented  
✅ Test changes locally before committing  
✅ Update documentation in the same commit  
✅ Use descriptive commit messages  
✅ Follow existing code patterns  
✅ Document decisions and trade-offs

---

## 📞 Quick Reference Links

**Live Showcase:** https://micha2718l.github.io/dolphain/showcase.html  
**Repository:** https://github.com/micha2718l/dolphain  
**Local Showcase:** http://localhost:8000/showcase.html (when running server)

---

## 🎯 Common Tasks Reference

### "Fix a bug in the showcase"

1. Read: `AUDIO_PLAYER_FIX.md` or `SHOWCASE_QUICK_REF.md`
2. Check: `site/js/audio-player.js` or `site/js/showcase.js`
3. Test: Run local server, test in browser
4. Document: Update relevant docs
5. Commit: Descriptive message with files changed

### "Improve detection algorithm"

1. Read: `CHIRP_CLICK_DETECTION.md`, `CONSERVATIVE_DETECTION.md`
2. Check: `scripts/quick_find.py` (detect_chirps, detect_click_trains)
3. Test: Run on sample files, check false positive rate
4. Document: Update algorithm docs with changes
5. Consider: Backward compatibility with existing results

### "Generate new showcase"

1. Check: External drive mounted? (`ls /Volumes/`)
2. Run: `scripts/quick_find.py` to find interesting files
3. Generate: `scripts/generate_showcase.py --checkpoint results.json`
4. Test: View locally, check all features work
5. Deploy: Commit and push to update GitHub Pages

### "Update documentation"

1. Check: `DOC_INDEX.md` for relevant docs
2. Edit: Keep START_HERE.md and CURRENT_STATUS.md current
3. Archive: Move outdated docs to `docs/archive/` (don't delete)
4. Test: Read through to ensure accuracy
5. Commit: "docs: update [topic]" with clear description

---

## 🎓 Learning Resources

- **PyWavelets:** https://pywavelets.readthedocs.io/
- **Web Audio API:** https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API
- **Spectrogram basics:** Frequency (y-axis) vs Time (x-axis) vs Power (color)
- **GitHub Pages:** https://pages.github.com/

---

**TL;DR for New Sessions:**

1. Read `START_HERE.md` (2 min) and `HANDOFF_NOTES.md` (10 min)
2. Check `CURRENT_STATUS.md` for latest state
3. Use `DOC_INDEX.md` to find relevant docs
4. Test locally before committing (`python3 -m http.server 8000`)
5. Keep code modular, documentation updated, git clean
6. Be direct, technical, show examples
7. User values clean code, good docs, and conservative detection

**You're ready to help!** 🚀
