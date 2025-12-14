# 📢 Dolphain Launch Content Plan

## 1. Hacker News (The "Show HN")

**Goal:** Reach developers and tech enthusiasts.
**Title:** Show HN: Dolphain – Dolphin bioacoustics in the browser (Python/WASM, co-written by AI)
**Url:** https://dolphain.mantilabs.ai/
**Text:**

> Hi HN,
>
> I've been building a Python toolkit for analyzing underwater acoustic recordings (specifically from the Gulf of Mexico) to understand dolphin communication.
>
> Two things make this project unique:
>
> 1. **The Tech:** It runs a full scientific Python stack (NumPy, SciPy, PyWavelets) entirely in the browser using Pyodide. You can load binary hydrophone data, apply wavelet denoising, and detect clicks/whistles client-side.
>
> 2. **The Experiment:** This is a study in "Human + AI" software development. The entire codebase, documentation, and this website were co-created with LLMs (Copilot/Gemini) acting as research assistants. We're trying to be radically transparent about this workflow to see if AI can accelerate scientific software.
>
> **Key Features:**
>
> - **Dolphain Studio:** Browser-based IDE for signal processing on real EARS data.
> - **Showcase:** A gallery of "interesting" signals found by our scoring algorithms (spectral entropy + harmonic spread).
> - **Open Data:** Built on the LADC-GEMM dataset (Gulf of Mexico Research Initiative).
>
> The goal is to make bioacoustics accessible to developers who might want to help decode these patterns, while exploring how AI can accelerate scientific software.
>
> Repo: https://github.com/micha2718l/dolphain
> Demo: https://dolphain.mantilabs.ai/portal/index.html
>
> Would love feedback on the signal processing pipeline, the WASM performance, or the AI-assisted workflow!

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

## 5. Brand Assets (Profile Pictures)

I've generated several custom profile picture options for the `@dolphain` X account using Python and Matplotlib. You can find them in `outputs/social_assets/`.

### Original Concepts

1.  **`profile_chirp_wave.png`**: A stylized "chirp" signal (sine wave with increasing frequency) glowing in cyan against a deep ocean background.
2.  **`profile_fin_spectrogram.png`**: A dolphin fin shape constructed from horizontal spectrogram lines.
3.  **`profile_minimal_d.png`**: A minimal geometric logo featuring a stylized "D" made of waves.

### New Iterations

4.  **`profile_chirp_spiral.png`**: A chirp signal wrapped into a spiral, creating a "portal" or "eye" effect. Very sci-fi.
5.  **`profile_chirp_pod.png`**: Three overlapping chirps in different shades (cyan, teal, white) representing a pod of dolphins communicating.
6.  **`profile_fin_dots.png`**: A fin shape made of thousands of scattered data points. Represents "data-driven biology".
7.  **`profile_fin_neon.png`**: A retro-futuristic neon outline of a fin with a grid fill.
8.  **`profile_fin_spectrogram_v2.png`**: An enhanced version of the fin spectrogram with a richer color gradient (Deep Blue → Cyan → Foam) and a hidden "pulse" ring embedded in the wave distortions.

**Recommendation:**

- **Tech/Sci-Fi:** `profile_chirp_spiral.png` or `profile_chirp_wave.png`
- **Biology/Data:** `profile_fin_spectrogram_v2.png` (Best balance of art & science)
- **Clean Brand:** `profile_minimal_d.png`

## 6. Launch Strategy for @dolphain_lab

### 📌 Pinned Tweet (The "Manifesto")

**Text:**

> 🐬 Meet Dolphain: Open-source toolkit for dolphin bioacoustics.
>
> 🌊 Analyze Gulf of Mexico data
> 💻 Run Python/SciPy in-browser (WASM)
> 🧪 Human + AI experiment
>
> Hunt for signals in the Studio:
> https://dolphain.mantilabs.ai/
>
> #Python #OpenScience #Pyodide

**Media:** Attach a video or screenshot of the "Dolphain Studio" in action (showing the spectrogram scrolling).

### 👥 Initial Accounts to Follow

Building a relevant network is key. Here are the top accounts to follow immediately:

1.  **@Pyodide** - The core technology powering the browser-based Python analysis.
2.  **@DOSITS_org** (Discovery of Sound in the Sea) - The authority on underwater acoustics.
3.  **@WHOI** (Woods Hole Oceanographic Institution) - Leaders in marine research and bioacoustics.
4.  **@NOAAFisheries** - Major source of marine mammal data and research.
5.  **@HuggingFace** - Where we host/plan to host datasets and models.
6.  **@NumFOCUS** - The non-profit behind NumPy, SciPy, and Project Jupyter.
7.  **@RealPython** - Great community for Python projects; they often highlight cool tools.
8.  **@Scripps_Ocean** - Another major institution for oceanography and acoustics.
9.  **@simonw** (Simon Willison) - Influential voice in "AI Engineering" and open source data tools.
10. **@OpenOceanSci** - Promoting open ocean science and data.
