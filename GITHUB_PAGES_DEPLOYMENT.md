# GitHub Pages Deployment Guide

This repository includes a custom landing page (`index.html`) designed to be deployed with GitHub Pages.

## 🌊 Live Site

Once deployed, the site will be available at:
**https://dolphain.mantilabs.ai/**

## 🚀 Quick Deployment Steps

### 1. Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/micha2718l/dolphain
2. Click on **Settings** (top right)
3. Scroll down to **Pages** (left sidebar under "Code and automation")
4. Under **Source**, select:
   - **Branch:** `main`
   - **Folder:** `/ (root)`
5. Click **Save**

### 2. Wait for Deployment

- GitHub will automatically build and deploy your site
- This usually takes 1-2 minutes
- You'll see a green checkmark when ready
- Visit: https://dolphain.mantilabs.ai/

### 3. Custom Domain (Optional)

If you have a custom domain:

1. In the **Custom domain** section, enter your domain
2. Add the appropriate DNS records (GitHub will provide instructions)

## 🎨 About the Landing Page

The `index.html` file is a self-contained, single-page site featuring:

- **Ocean-themed design** with animated bubbles
- **Dolphin science facts** and communication research
- **Quick start guide** for the Dolphain library
- **Hitchhiker's Guide to the Galaxy** inspired elements
- **Easter egg:** Click the "42" button in the corner!
- **Fully responsive** mobile-friendly design

### Design Philosophy

- No generic AI purple gradients 🚫
- Ocean blues and natural coastal colors 🌊
- Clean, readable typography
- Animated but performant
- Accessible and semantic HTML

## 📝 Customization

To modify the landing page:

1. Edit `index.html` in the repository root
2. Commit and push changes
3. GitHub Pages will automatically rebuild

All styles and scripts are embedded in the HTML file for simplicity.

## 🔧 Local Development

To preview locally:

```bash
# Simple Python server
python3 -m http.server 8000

# Or with Node.js
npx http-server

# Then open: http://localhost:8000
```

## 📚 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Custom Domain Setup](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)
- [Jekyll Themes](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll) (if you want to use Jekyll instead)

## 🐬 Features on the Landing Page

- **Project Overview:** What Dolphain is and why it exists
- **Features Grid:** Core capabilities of the library
- **Quick Start:** Installation and basic usage examples
- **Science Section:** Dolphin communication facts and statistics
- **Research Progress:** Current state and achievements
- **Call-to-Action:** Links to GitHub, docs, and contribution guide

---

**Note:** The landing page uses no external dependencies (no jQuery, no Bootstrap, no external CSS). Everything is self-contained for maximum reliability and fast loading.

🐬 Happy deploying! Don't forget your towel! 🐬
