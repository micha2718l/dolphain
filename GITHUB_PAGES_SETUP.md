# GitHub Pages Configuration

## Setup Instructions

To deploy the Dolphain landing page:

1. Go to your repository settings: `https://github.com/micha2718l/dolphain/settings/pages`
2. Under "Build and deployment":
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/site` (NOT root `/`)
3. Click "Save"

GitHub Pages will automatically deploy from the `/site` directory.

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

After committing and pushing changes, GitHub Pages will automatically rebuild (usually within 1-2 minutes).

## Files Removed

- ~~`/index.html`~~ - Old root file, now removed (use `/site/index.html`)
- All website files now properly organized in `/site/`
