data = dolphain.read_ears_file('file.210')
dolphain.plot_overview(data, fmax=5000)
denoised = dolphain.wavelet_denoise(data['data'])
#! Dolphain Project – Status & Roadmap

**Last Updated:** October 10, 2025 (Threshold sweep & special-file comparison)

---

## 📌 Executive Summary

- **Core library is stable and production ready.** All modules (`io`, `signal`, `plotting`, `batch`) are tested and documented.
- **Research notebooks are evolving.** Click-detection experiments now include runtime guardrails, special-file comparisons, and threshold sweeps (4/6/8) with persisted metrics and plots.
- **Data estate expanded.** In addition to the 100 buoy recordings, two “special” files (`71621DC7 (1).190`, `7164403B.130`) are available for comparative studies.

The project is ready for new research directions (whistle detection, advanced click quality metrics) while maintaining a robust base package for wider adoption.

---

## �️ Core Library Snapshot

| Area                                  | Status       | Notes                                                         |
| ------------------------------------- | ------------ | ------------------------------------------------------------- |
| File I/O (`dolphain.io`)              | ✅ Stable    | Reads `.130`, `.190`, `.210`; metadata helpers intact         |
| Signal Processing (`dolphain.signal`) | ✅ Stable    | Wavelet denoising (VisuShrink), threshold utilities           |
| Plotting (`dolphain.plotting`)        | ✅ Stable    | Waveform, spectrogram, denoising comparisons                  |
| Batch Framework (`dolphain.batch`)    | ✅ Stable    | `BatchProcessor`, `ResultCollector`, discovery helpers, timer |
| Tests                                 | ✅ Passing   | `tests/test_ears_reader.py`, `test_batch.py`                  |
| CLI                                   | ✅ Available | `ears_cli.py` for quick conversions/info                      |

Documentation for the core package remains accurate: `README.md`, `BATCH_PROCESSING.md`, and `BATCH_IMPLEMENTATION.md` require no structural changes beyond cross-references captured below.

---

## � Research & Experiments

| Notebook                                        | Focus                          | Latest Highlights (Oct 2025)                                                                                                    |
| ----------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| `examples/dolphin_communication_analysis.ipynb` | Dolphin click/whistle research | Added runtime guardrails, chunked click detection, special-file comparison, threshold sweep (4/6/8) with CSV outputs and plots. |
| `examples/batch_experiments.ipynb`              | Batch-framework demos          | Stable reference for running pipelines over many files.                                                                         |
| `examples/ears_analysis_demo.ipynb`             | Quickstart                     | No changes this cycle.                                                                                                          |

Persisted artifacts for reproducibility:

- `reports/click_preview_top10.csv`
- `reports/click_comparison_buoy_vs_special.csv`
- `reports/click_threshold_sweep_details.csv`
- `reports/click_threshold_sweep_summary.csv`

---

## 📁 Repository Structure (2025-10-10)

```
dolphain/
├── dolphain/                  # Core library modules
├── examples/                  # Research & demo notebooks
├── tests/                     # Automated tests
├── data/
│   ├── Buoy210_100300_100399/ # 100 buoy recordings (*.210)
│   └── special/               # 2 comparative recordings (*.130, *.190)
├── reports/                   # CSV outputs from recent experiments
├── docs/                      # README + batch documentation
└── support files              # CLI, setup.py, requirements.txt, etc.
```

---

## 📊 Current Insights from Experiments

- **Click Detection (5 s chunks, threshold=4):**

  - Buoy sample (n=10) averages 2,325 detections (465 clicks/s) with median ICI ≈ 0.148 ms.
  - Special files (n=2) average 446 detections (89 clicks/s) with median ICI ≈ 0.219 ms.

- **Threshold Sweep (4 → 6 → 8):**

  - Buoy detections retain ~37% of baseline at threshold 6 and ~22% at threshold 8 (still non-zero, indicating stronger signals).
  - Special files collapse to <5% at threshold 6 and ≈1% at threshold 8, suggesting many low-threshold hits were noise-like.
  - Visual summaries: “Mean Click Rate vs Threshold” and “Detection Retention by File”.

- **Runtime Guardrails:** `RuntimeGuard`, `timed_block`, and `iterate_chunks` utilities prevent runaway cells; all processing reported <0.25 s per file in recent runs.

---

## 🧭 Next Steps (Prioritized)

1. **Click Quality Refinement**

   - Investigate high-count buoy files to confirm genuine dolphin clicks (spectral slices, waveform overlays).
   - Experiment with adaptive smoothing windows and alternative energy operators to reduce false positives without losing true clicks.

2. **Chunk-Wise Trend Analysis**

   - Use `iterate_chunks` to sample additional time windows per file, logging per-chunk statistics to the `reports/` directory for temporal stability checks.

3. **Whistle Detection Scaffold**

   - Implement the Section 2.2 plan: band-pass (2–20 kHz), spectrogram ridge tracking, contour extraction, and duration filtering.
   - Prepare storage schema for whistle contour metadata (JSON/CSV).

4. **Batch Integrations**

   - Wrap the click/whistle detectors into batch pipelines so full datasets (100+ files) can be processed with summary dashboards.

5. **Documentation & Packaging**
   - Promote new reports and guardrails in `README.md` (analysis section) and keep `docs/` aligned as whistle work lands.
   - Evaluate packaging extras (e.g., optional dependency set for notebooks).

---

## 🧾 Reference Documents (Updated)

| Document                  | Purpose                            | Current Action                                                                         |
| ------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------- |
| `README.md`               | Core library overview & quickstart | Add link to dolphin communication notebook + reports directory (see commit checklist). |
| `BATCH_PROCESSING.md`     | Batch framework how-to             | No changes required.                                                                   |
| `BATCH_IMPLEMENTATION.md` | Architectural notes                | No changes required.                                                                   |
| `SESSION_STATE.md`        | Day-to-day continuation log        | Updated with guardrails, click comparison, threshold sweep, and outstanding tasks.     |
| `NEXT_STEPS.md`           | Actionable plan for users          | Updated (see separate document).                                                       |

---

## ✅ Validation & Quality Gates

- **Unit Tests:** `pytest` suite green (manual confirmation last run prior to session; rerun before release).
- **Notebook Cells:** Latest click detection, special-file comparison, and threshold sweep executed without errors (<8 s for entire sweep).
- **Artifacts:** Reports persisted under `reports/` and referenced in documentation.

---

## 📣 Ready for Contributions

- Issues/PRs welcome for whistle detection, classifier prototypes, or visualization enhancements.
- For new analyses, replicate the guardrail pattern (≤5 s chunks, bounded runtime, CSV/plot outputs).

---

## � Quick Links

- Core API overview – `README.md`
- Batch how-to – `docs/BATCH_PROCESSING.md`
- Latest research notebook – `examples/dolphin_communication_analysis.ipynb`
- Experiment outputs – `reports/`

---

**Bottom line:** The Dolphain library remains stable and documented, while the research workspace now includes reproducible click-detection experiments, special-file comparisons, and threshold analyses—setting the stage for whistle detection and richer behavioral insights.
