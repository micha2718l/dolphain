# 🔧 Showcase & Deployment Fixes

## Issue 1: Showcase CORS Error ✅ FIXED

### Problem:
Opening `showcase.html` with `file://` protocol causes CORS errors blocking JSON loading.

### Solution Applied:
Added helpful error message that detects CORS issues and provides instructions.

### To View Showcase Locally:
```bash
cd site/showcase
python -m http.server 8000
```
Then visit: http://localhost:8000/showcase.html

**OR** (from project root):
```bash
cd site
python -m http.server 8000
```
Then visit: http://localhost:8000/showcase/showcase.html

---

## Issue 2: GitHub Pages URL Structure

### Current Behavior:
- Main URL shows README.md
- Site is at `/site` subdirectory

### Expected Behavior:
- Main URL should show `index.html` from site/
- Showcase at `/showcase.html`

### Root Cause:
The workflow uploads `./site` directory, so contents should be at root. However, GitHub Pages might be configured to use root instead of the artifact.

### Fix Options:

#### Option A: Verify GitHub Pages Settings (Recommended)
1. Go to: https://github.com/micha2718l/dolphain/settings/pages
2. Check "Source" setting:
   - Should be: **GitHub Actions** (not "Deploy from a branch")
3. If it says "Deploy from a branch", change to "GitHub Actions"

#### Option B: Update Workflow (If needed)
If Pages settings are correct but still not working, the workflow is fine as-is. The artifact upload already uses `./site`.

#### Option C: Add Base Path Config
If you want to keep the URL structure as `/site`, add this to your workflow:

```yaml
# In .github/workflows/deploy-pages.yml
# After line 41 (path: "./site"), add:
        with:
          path: "./site"
          # retention-days: 1  # Optional: reduce artifact storage
```

---

## Issue 3: Showcase Data Path

### For Deployment:
The showcase expects `showcase_data.json` in the same directory as `showcase.html`.

**Current structure (correct):**
```
site/
├── index.html
├── showcase.html
├── showcase_data.json  ← Must be here
└── showcase/
    ├── audio/
    ├── images/
    └── showcase_data.json  ← Also here for direct access
```

### Fix: Copy showcase.html to site root

```bash
# The showcase.html should be at site/showcase.html
# Data should be at site/showcase/showcase_data.json
# But HTML looks for showcase_data.json in same directory

# So either:
# 1. Keep showcase.html in site/showcase/ (current location)
# 2. OR update the path in showcase.html
```

Let me check your current structure:
```bash
ls -la site/
ls -la site/showcase/
```

---

## Quick Fix Commands:

### 1. Test Showcase Locally:
```bash
cd site
python -m http.server 8000
# Visit: http://localhost:8000/showcase.html
```

### 2. Check GitHub Pages Status:
Visit: https://github.com/micha2718l/dolphain/actions

Look for the latest "Deploy Dolphain Site to GitHub Pages" workflow run.

### 3. Force Re-deploy:
```bash
# Trigger workflow manually
git commit --allow-empty -m "Trigger Pages deployment"
git push
```

---

## Correct URLs After Deployment:

Based on your workflow, URLs should be:
- Main site: `https://github.colorsynth.systems/dolphain/`
- Showcase: `https://github.colorsynth.systems/dolphain/showcase.html`

If you're seeing README instead, check:
1. GitHub Pages source setting (must be "GitHub Actions")
2. Workflow ran successfully
3. No custom domain config overriding

---

## Testing Checklist:

- [ ] Showcase loads locally with `python -m http.server`
- [ ] Showcase data.json loads (no CORS errors)
- [ ] Audio players work
- [ ] Images display
- [ ] GitHub Pages source is "GitHub Actions"
- [ ] Latest workflow completed successfully
- [ ] Main URL shows index.html (not README.md)
- [ ] Showcase accessible at /showcase.html

---

## Next Steps:

1. **Test locally first:**
   ```bash
   cd site
   python -m http.server 8000
   open http://localhost:8000/showcase.html
   ```

2. **Check GitHub Pages settings** at repo settings

3. **Review latest Actions run** for any errors

4. **If still broken after these fixes**, provide:
   - Screenshot of GitHub Pages settings
   - Output of latest Actions workflow
   - Current URL structure you're seeing
