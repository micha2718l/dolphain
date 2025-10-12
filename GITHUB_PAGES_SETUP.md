# GitHub Pages Configuration

## 🚀 Automated Deployment with GitHub Actions

The Dolphain site automatically deploys from the `/site` directory using GitHub Actions!

### One-Time Setup (You Need To Do This!)

1. **Go to your repository settings**: https://github.com/micha2718l/dolphain/settings/pages

2. **Under "Build and deployment"**:

   - **Source**: Select **"GitHub Actions"** (NOT "Deploy from a branch")
   - That's it! The workflow file will handle the rest.

3. **Verify Permissions** (should be automatic, but check):
   - Go to https://github.com/micha2718l/dolphain/settings/actions
   - Under "Workflow permissions", ensure:
     - ✅ "Read and write permissions" is selected, OR
     - ✅ "Read repository contents and packages permissions" with Pages write access
4. **Push this commit** to trigger the first deployment!

### How It Works

The workflow file at `.github/workflows/deploy-pages.yml` will:

- ✅ Automatically trigger on pushes to `main` branch
- ✅ Only run when files in `/site` directory change
- ✅ Deploy the `/site` directory contents to GitHub Pages
- ✅ Complete deployment in ~30-60 seconds

No manual deployment needed! Just push and it goes live.

## Site Structure

```
/site/
  ├── index.html              # Main landing page
  ├── dolphin-composer.html   # Interactive sound composer
  ├── DATA_ATTRIBUTION.html   # Attribution page (if exists)
  ├── css/
  │   └── style.css          # Main stylesheet
  ├── js/
  │   └── script.js          # Interactive features
  └── images/
      ├── waveform.png       # Example visualizations
      ├── spectrogram.png
      └── denoising.png
```

## Live URL

Once configured, the site will be available at:
**https://micha2718l.github.io/dolphain/**

## Local Testing

To test the site locally:

```bash
# Option 1: Simple Python server
cd site
python -m http.server 8000
# Visit http://localhost:8000

# Option 2: Open directly in browser (limited functionality)
open site/index.html
```

## Why /site Directory?

- **Clean separation**: Keep website separate from code
- **Organized**: All web assets in one place
- **Standard practice**: Common pattern for GitHub Pages
- **Easy deployment**: Point and forget

## Updating the Site

All changes to the website should be made in the `/site` directory:

- Edit `/site/index.html` for landing page changes
- Edit `/site/css/style.css` for styling
- Edit `/site/js/script.js` for interactive features
- Add images to `/site/images/`

After committing and pushing changes:

1. GitHub Actions workflow automatically triggers
2. Deployment completes in ~30-60 seconds
3. Site updates live at https://micha2718l.github.io/dolphain/

You can watch the deployment progress at:
https://github.com/micha2718l/dolphain/actions

## Workflow Details

The workflow (`.github/workflows/deploy-pages.yml`):

- **Triggers on**: Push to `main` branch with changes in `/site/**`
- **Can also**: Run manually from Actions tab
- **Permissions**: Reads code, writes to Pages, uses id-token
- **Concurrency**: Only one deployment at a time (no conflicts)
- **Steps**:
  1. Checkout repository
  2. Setup GitHub Pages
  3. Upload `/site` directory as artifact
  4. Deploy artifact to GitHub Pages

## Troubleshooting

### First Deployment Not Working?

1. Check that you selected "GitHub Actions" as source in Pages settings
2. Go to Actions tab and check if workflow ran: https://github.com/micha2718l/dolphain/actions
3. Check workflow permissions in repository settings

### Site Not Updating After Push?

1. Verify your changes were in the `/site/` directory
2. Check Actions tab for workflow status
3. Workflow only runs if `/site/**` files changed (by design - efficient!)

### Manual Deployment Needed?

1. Go to https://github.com/micha2718l/dolphain/actions
2. Click on "Deploy Dolphain Site to GitHub Pages"
3. Click "Run workflow" button
4. Select `main` branch and run

## Files Removed

- ~~`/index.html`~~ - Old root file, now removed (use `/site/index.html`)
- All website files now properly organized in `/site/`
