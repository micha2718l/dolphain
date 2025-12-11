# 🗺️ Dolphain Project Roadmap

Welcome to the Dolphain project! This document outlines our current capabilities, our future goals, and how you can get involved. Whether you're a marine biologist, a data scientist, or a curious developer, there's a place for you here.

## 🟢 What We Can Do Now (Current Capabilities)

As of December 2025, Dolphain is a robust toolkit for acoustic analysis:

- **Data Ingestion**: Read and parse binary EARS data files (.130, .190, .210) efficiently.
- **Signal Processing**:
  - **Wavelet Denoising**: Clean noisy underwater recordings using VisuShrink thresholding.
  - **Spectrogram Generation**: Create high-resolution time-frequency visualizations.
- **Detection Algorithms**:
  - **Conservative Detection**: High-precision identification of clicks and chirps with minimal false positives.
  - **Unique Signal Detection**: A scoring system to find "interesting" or unusual acoustic events based on spectral entropy and harmonic structure.
- **Interactive Tools**:
  - **Dolphain Studio**: A browser-based environment to run Python analysis code on real data without installation.
  - **Showcase**: A curated gallery of the most interesting signals found so far.

## 🟡 What We Want To Do (Future Goals)

We have big plans to expand our understanding of dolphin communication:

### 1. Advanced Classification (The "Rosetta Stone" Goal)

- **Cluster Analysis**: Automatically group similar whistles and clicks to identify "vocabulary".
- **Signature Whistle ID**: Track individual dolphins across different recordings.
- **Machine Learning**: Train deep learning models (CNNs/Transformers) on our labeled data for better classification.

### 2. Infrastructure & Scale

- **Cloud Processing**: Scale our batch processing to handle terabytes of GoMRI data in the cloud.
- **Real-time Analysis**: Optimize algorithms to run on edge devices (buoys) for real-time monitoring.

### 3. Community & Education

- **Educational Notebooks**: Create a series of Jupyter notebooks teaching the basics of bioacoustics signal processing.
- **Citizen Science**: Build a tool for users to help label and verify detections.

## 🧪 Cool Things To Play With

If you're just exploring, here are some fun things to try:

1.  **The Studio**: Go to [Dolphain Studio](https://micha2718l.github.io/dolphain/portal/index.html) and try the "Denoising" example. See if you can tune the parameters to make the whistles clearer!
2.  **Branch Explorer**: Check out the [Branch Explorer](https://micha2718l.github.io/dolphain/branch_explorer/) to see how our detection algorithms make decisions.
3.  **Composer**: Use the [Dolphin Composer](https://micha2718l.github.io/dolphain/dolphin-composer.html) to arrange dolphin sounds into music (just for fun!).

## 🤝 How To Contribute

We want your help!

- **For Developers**: Check the `issues` tab on GitHub. We need help with optimization, UI improvements, and new feature implementation.
- **For Scientists**: We need help validating our detections. Are we finding clicks or shrimp noise? Let us know!
- **For Learners**: Read through the code in `dolphain/signal.py`. It's heavily commented to explain _why_ we do things, not just _how_.

---

_“So long, and thanks for all the fish data.”_
