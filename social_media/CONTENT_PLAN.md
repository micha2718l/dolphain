# 📢 Dolphain Launch Content Plan

## 1. Hacker News (The "Show HN")

**Goal:** Reach developers and tech enthusiasts.
**Title:** Show HN: Dolphain – Analyze dolphin acoustics in your browser with Python/WASM
**Url:** https://dolphain.mantilabs.ai/
**Text:**

> Hi HN, I've been working on a Python toolkit for analyzing underwater acoustic recordings (specifically from the Gulf of Mexico) to understand dolphin communication.
>
> It includes:
>
> 1. **Dolphain Studio:** A browser-based environment (using Pyodide) where you can run real Python signal processing code on the data without installing anything.
> 2. **Showcase:** A gallery of the most "interesting" signals found so far, ranked by a custom uniqueness metric (spectral entropy + harmonic spread).
> 3. **Python Library:** For wavelet denoising, click detection, and spectral analysis.
>
> The goal is to make bioacoustics accessible to developers and data scientists who might want to help decode these patterns.
>
> Repo: https://github.com/micha2718l/dolphain
> Demo: https://dolphain.mantilabs.ai/portal/index.html
>
> Would love feedback on the signal processing pipeline or the WASM implementation!

## 2. Reddit (r/Python)

**Title:** I built a tool to analyze dolphin sounds in the browser using Pyodide and Python
**Text:**

> Hey r/Python,
>
> I wanted to share a project I've been working on called **Dolphain**. It's a toolkit for analyzing underwater acoustic data to study dolphin communication.
>
> **The Cool Part:**
> I built a "Studio" that runs the full Python analysis pipeline (NumPy, SciPy, Matplotlib) entirely in the browser using **Pyodide**. You can load binary hydrophone data, apply wavelet denoising, and detect clicks/whistles right in Chrome/Firefox.
>
> **Features:**
>
> - **Wavelet Denoising:** Cleans up noisy ocean recordings.
> - **Click Detection:** Finds echolocation clicks using Teager-Kaiser energy operators.
> - **Interactive Plots:** Matplotlib charts rendered to the DOM.
>
> **Links:**
>
> - **Try the Studio:** https://dolphain.mantilabs.ai/portal/index.html
> - **GitHub:** https://github.com/micha2718l/dolphain
>
> I'm looking for contributors interested in signal processing or AI to help improve the classification algorithms!

## 3. Twitter / X

**Tweet 1 (The Hook):**

> 🐬 Ever wanted to decode dolphin language?
>
> I built Dolphain – an open-source Python toolkit for bioacoustics.
>
> 🌊 Analyze underwater sounds
> 💻 Run Python in your browser (WASM)
> 🤖 Hunt for unique signals with AI
>
> Try it now: https://dolphain.mantilabs.ai/portal/index.html
>
> #Python #OpenScience #MarineBiology #Pyodide

**Tweet 2 (The Tech):**

> Under the hood, Dolphain uses:
> 🔹 PyWavelets for denoising
> 🔹 SciPy for signal processing
> 🔹 Pyodide to run it all in the browser
>
> Check out the code: https://github.com/micha2718l/dolphain
>
> #DataScience #SignalProcessing

## 4. Marine Biology Communities (LinkedIn / r/marinebiology)

**Title:** Open Source Tool for Acoustic Analysis
**Text:**

> Hello everyone,
>
> I'm sharing an open-source project designed to make acoustic analysis more accessible. **Dolphain** allows you to visualize and analyze EARS data files directly in a web browser, no complex installation required.
>
> We're looking for feedback from biologists:
>
> 1. Are our detection algorithms picking up biologically significant events?
> 2. How can we make the visualization tools more useful for your research?
>
> Try the showcase here: https://dolphain.mantilabs.ai/showcase.html
