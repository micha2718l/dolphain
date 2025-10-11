# Dolphain GitHub Pages Site

This directory contains the GitHub Pages website for the Dolphain project.

## Structure

```
site/
├── index.html              # Main landing page
├── css/
│   └── style.css          # Stylesheet (ocean theme)
├── js/
│   └── script.js          # Interactive features
├── images/
│   ├── waveform.png       # Example waveform visualization
│   ├── spectrogram.png    # Example spectrogram
│   └── denoising.png      # Example denoising comparison
└── DATA_ATTRIBUTION.md    # Data sources and credits
```

## Deployment

### GitHub Pages Setup

1. Go to repository Settings → Pages
2. Under "Source", select:
   - **Branch:** `main`
   - **Folder:** `/site`
3. Click **Save**
4. Visit: https://micha2718l.github.io/dolphain/

### Local Testing

```bash
cd site
python3 -m http.server 8000
# Visit: http://localhost:8000
```

## Features

- **Real Examples:** All visualizations are generated from actual EARS data files
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Interactive:** Floating bubbles, smooth scrolling, easter eggs
- **Ocean Theme:** Custom color palette inspired by underwater research
- **H2G2 References:** Hitchhiker's Guide to the Galaxy easter eggs

## Regenerating Examples

To update the example images:

```bash
# From the project root
python generate_examples.py
```

This will regenerate all images in `site/images/` from the sample data file.

## Attribution

- **Research & Analysis:** Michael Haas (University of New Orleans, Physics)
- **Website & Documentation:** Created with GitHub Copilot (AI assistance)
- **Data Source:** LADC-GEMM consortium, funded by GoMRI
- **Design Theme:** Custom ocean-inspired palette (no generic AI purple!)
- **Inspiration:** Douglas Adams' "The Hitchhiker's Guide to the Galaxy"

## Technical Details

- **Framework:** Vanilla HTML/CSS/JavaScript (no dependencies)
- **Styling:** CSS variables, responsive grids, GPU-accelerated animations
- **Accessibility:** WCAG AA compliant, semantic HTML, keyboard navigation
- **Performance:** Single CSS/JS files, optimized images, lazy loading

---

🐬 "So long, and thanks for all the fish data" 🐬
