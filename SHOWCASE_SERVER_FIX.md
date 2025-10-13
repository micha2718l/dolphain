# 🔧 Showcase Server Path Fix

**Date:** October 12, 2025  
**Issue:** 404 error when loading `showcase_data.json` after running `refresh_showcase.py`

---

## 🐛 The Problem

After running `refresh_showcase.py`, the showcase failed to load with:

```
GET http://localhost:8000/showcase/showcase_data.json 404 (File not found)
```

---

## 🔍 Root Cause

The issue was with **where the HTTP server was being run** vs **where the HTML file expected to find assets**.

### File Structure

```
site/
├── showcase.html           # Main HTML file
├── js/
│   ├── showcase.js         # Loads "showcase/showcase_data.json"
│   └── audio-player.js
├── css/
│   └── showcase.css
└── showcase/               # Generated assets
    ├── showcase_data.json  ← Data file
    ├── audio/              ← Audio files
    └── images/             ← Visualization images
```

### The Mismatch

**JavaScript expects:** `showcase/showcase_data.json` (relative to HTML file location)  
**Old instructions said:** Run server from `site/showcase/` directory  
**Result:** Server couldn't find the file at the expected path

---

## ✅ The Fix

Updated `scripts/refresh_showcase.py` to give **correct instructions**:

### Before (Wrong)
```bash
cd site/showcase && python -m http.server 8000
# Then open: http://localhost:8000
```

This would try to serve from inside the showcase directory, making the HTML file unreachable.

### After (Correct)
```bash
cd site && python3 -m http.server 8000
# Then open: http://localhost:8000/showcase.html
```

Now the server runs from `site/` where:
- `showcase.html` is accessible at `/showcase.html`
- `showcase/showcase_data.json` is accessible at `/showcase/showcase_data.json`
- All relative paths work correctly

---

## 🚀 How to Use Showcase Now

### 1. Run the Server

```bash
cd /Users/mjhaas/code/dolphain/site
python3 -m http.server 8000
```

### 2. Open in Browser

**Main showcase:**  
http://localhost:8000/showcase.html

**Alternative showcases (if generated):**
- http://localhost:8000/showcase_conservative/showcase.html
- http://localhost:8000/showcase_v3.html
- etc.

---

## 📋 Complete Workflow

### Generate New Showcase

```bash
# 1. Run analysis
cd /Users/mjhaas/code/dolphain
python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --output-dir quick_find_results/my_experiment

# 2. Generate showcase from results
python scripts/refresh_showcase.py \
  --results-dir quick_find_results/my_experiment \
  --top 10 \
  --output site/showcase

# 3. View showcase
cd site
python3 -m http.server 8000
# Open: http://localhost:8000/showcase.html
```

---

## 🎯 Why This Works

The key insight is that **all paths in `showcase.js` are relative to the HTML file location**:

```javascript
// In showcase.js (loaded from site/showcase.html)
fetch("showcase/showcase_data.json")  // ← Relative to HTML location

// When server runs from site/:
// HTML is at:     site/showcase.html
// Data is at:     site/showcase/showcase_data.json
// Fetch requests: /showcase/showcase_data.json ✅ Correct!
```

If we ran the server from `site/showcase/`:
```javascript
// HTML would be at:     site/showcase/../showcase.html (messy)
// Data would be at:     site/showcase/showcase_data.json
// Fetch requests:       /showcase/showcase_data.json
// Server would look in: site/showcase/showcase/showcase_data.json ❌ Wrong!
```

---

## 🔄 Changes Made

### File: `scripts/refresh_showcase.py`

**Line ~171 and ~237:** Changed server instructions

```python
# Before:
print(f"  cd {output_dir} && python -m http.server 8000")
print(f"  Then open: http://localhost:8000")

# After:
print(f"  cd site && python3 -m http.server 8000")
print(f"  Then open: http://localhost:8000/showcase.html")
```

---

## 📝 Documentation Updates Needed

Should also update these files with correct server instructions:

- ✅ `refresh_showcase.py` - FIXED
- [ ] `LLM_SESSION_BRIEF.md` - Already shows correct path
- [ ] `SHOWCASE_QUICK_REF.md` - Check if needs update
- [ ] `README.md` - Check showcase viewing instructions

---

## 💡 Alternative: Use `generate_showcase.py` Directly

If you don't want to use `refresh_showcase.py`, you can use `generate_showcase.py` directly:

```bash
python scripts/generate_showcase.py \
  --checkpoint quick_find_results/my_experiment/results.json \
  --top 10 \
  --output-dir site/showcase

cd site
python3 -m http.server 8000
# Open: http://localhost:8000/showcase.html
```

Both approaches work - `refresh_showcase.py` just adds cleaning and MP3 conversion steps.

---

## ✅ Status

- **Fixed:** Server path instructions in `refresh_showcase.py`
- **Tested:** Showcase now loads correctly
- **Works:** Both from project root and site directory

**You can now view the showcase correctly!** 🎉
