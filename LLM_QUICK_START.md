# 🚀 Quick Start for New LLM Sessions

**30-Second Brief for helping with Dolphain project**

---

## What You Need to Know

**Project:** Dolphin acoustic analysis toolkit (Python + Web showcase)  
**Status:** Production ready, actively developed  
**Your Role:** Help with code, docs, debugging, improvements

---

## First 3 Things to Read

1. **`START_HERE.md`** (2 min) - Current status, what's working
2. **`HANDOFF_NOTES.md`** (10 min) - Complete technical overview
3. **`CURRENT_STATUS.md`** (3 min) - Latest state and next steps

**Everything else:** Use `DOC_INDEX.md` to navigate

---

## Key Architecture

```
dolphain/          # Python library (detection algorithms)
scripts/           # CLI tools (quick_find.py, generate_showcase.py)
site/              # Web showcase (HTML + CSS + JS)
  ├── showcase.html      # Main page (16 lines)
  ├── css/showcase.css   # Styling (150 lines)
  └── js/
      ├── audio-player.js  # Player class (194 lines)
      └── showcase.js      # UI logic (148 lines)
```

---

## What We Do

1. **Detect** dolphin vocalizations (chirps + click trains) in underwater recordings
2. **Score** files by "interestingness" (0-100 scale, conservative algorithm)
3. **Showcase** results in interactive web gallery with audio player

---

## User's Preferences

✅ Clean, modular code (<300 lines per file)  
✅ Comprehensive documentation  
✅ Good git hygiene (descriptive commits, proper .gitignore)  
✅ Conservative detection (fewer false positives)  
✅ Show examples and outputs, be direct and technical

---

## Common Commands

```bash
# View showcase
cd site && python3 -m http.server 8000
# → http://localhost:8000/showcase.html

# Analyze files
source .venv/bin/activate
python scripts/quick_find.py --file-list ears_files_list.txt --n-files 100

# Generate showcase
python scripts/generate_showcase.py --checkpoint results.json --top 10
```

---

## Important Notes

⚠️ **Don't commit:** EARS files (8MB each), test*\* dirs, temp*\* dirs  
⚠️ **External drive:** Source data on external drive (may not be mounted)  
⚠️ **User edits:** User makes manual edits - respect them, check files first  
⚠️ **Known issue:** Mode switching has 1-2sec seeking delay (documented)

---

## Quick Git Check

Before doing anything:

```bash
git status          # What's uncommitted?
git log -3 --oneline  # Recent commits
```

---

## When User Asks You To...

**Fix a bug:** Read relevant docs in `DOC_INDEX.md`, check current code, test locally, document fix  
**Add a feature:** Check architecture, keep it modular, update docs in same commit  
**Update docs:** Keep `START_HERE.md` and `CURRENT_STATUS.md` current, archive old docs  
**Generate showcase:** Check drive mounted, run quick_find → generate → test locally → commit

---

## Red Flags (Ask First)

🚨 Committing files >1MB  
🚨 Creating files >500 lines  
🚨 Breaking working features  
🚨 Skipping documentation updates  
🚨 Making major architecture changes

---

## Your Quick Checklist

1. ☐ Read START_HERE.md (2 min)
2. ☐ Read HANDOFF_NOTES.md (10 min)
3. ☐ Check git status
4. ☐ Understand the task
5. ☐ Check relevant docs (DOC_INDEX.md)
6. ☐ Make changes (test locally)
7. ☐ Update docs (same commit)
8. ☐ Commit with clear message

---

## TL;DR

Read `START_HERE.md` → Check `CURRENT_STATUS.md` → Use `DOC_INDEX.md` for navigation → Be modular, document well, test locally → You're ready! 🚀

**Full details:** See `LLM_SESSION_BRIEF.md`
