# Next Steps – October 2025 Roadmap

The## 🚀 How to Get Moving

1. **Read the continuation guide:**

   ```bash
   # Open CONTINUATION_GUIDE.md for complete instructions
   code CONTINUATION_GUIDE.md
   ```

2. **Load the notebook:**

   ```bash
   cd /Users/mjhaas/code/dolphain
   source .venv/bin/activate  # if needed
   jupyter notebook examples/dolphin_communication_analysis.ipynb
   ```

3. **Review current work:** Check which cells have execution counts and what variables are in memory.

4. **Choose your next task:** See CONTINUATION_GUIDE.md for detailed implementation plans.

Time required: 15–30 minutes to get oriented; 2-4 hours for whistle detection implementation.rary is stable; we’re now building higher-level analyses for dolphin communication. Use this guide to pick up the next piece of work quickly.

---

## ✅ What’s Already Solid

- **Library foundation:** `dolphain.io`, `signal`, `plotting`, and `batch` are production-ready with passing tests.
- **Batch toolkit:** `BatchProcessor`, `ResultCollector`, and helper utilities are documented in `BATCH_PROCESSING.md` and validated via `test_batch.py`.
- **Research notebook:** `examples/dolphin_communication_analysis.ipynb` now includes runtime guardrails, click detection on chunks, special-file comparisons, and threshold sweeps (4/6/8) with CSV outputs in `reports/`.
- **Artifacts:** Click preview, buoy vs special comparison, and threshold sweep reports persist in the repo for reproducible analysis.

---

## 🎯 Focus Areas

### 1. Click Detection Refinement

- Inspect high-count buoy files with waveform + spectrogram overlays to validate detections.
- Tweak smoothing windows and threshold factors (4/6/8 baseline) to reduce false positives without losing strong signals.
- Extend chunk iteration with `iterate_chunks` to capture temporal variability and log per-chunk metrics to `reports/`.

### 2. Whistle Detection Bootstrap

- Implement the Section 2.2 plan: band-pass 2–20 kHz, high-resolution spectrogram, ridge/contour extraction, ≥0.1 s duration filter.
- Define a lightweight data structure (DataFrame/JSON) for whistle contour metadata.
- Add placeholder visualizations for extracted contours to confirm quality.

### 3. Batch Integration

- Wrap refined click/whistle detectors in `BatchProcessor` pipelines so the 100 buoy files (and future datasets) can be processed automatically.
- Collect summary statistics (click rate, ICI, whistle counts) and persist to `reports/` for further analysis.

### 4. Documentation & Packaging

- Update `README.md` “Examples” section with links to the communication notebook and generated reports.
- Keep `PROJECT_STATUS.md` and this roadmap in sync after each milestone.
- Consider optional extras in `setup.py` for notebook-specific dependencies if new packages are introduced.

---

## 🚀 How to Get Moving

1. **Load the notebook:**
   ```bash
   jupyter notebook examples/dolphin_communication_analysis.ipynb
   ```
2. **Review the “Threshold Sensitivity” section** (Cells 17–19) to get familiar with the new outputs.
3. **Clone a chunk-analysis cell** and iterate on new parameter sets (e.g., different smoothing windows or frequency bands).
4. **Capture results:** Save CSVs/plots to `reports/` and note key findings in `SESSION_STATE.md`.

Time required: 15–30 minutes for a parameter experiment; longer for whistle prototyping.

---

## 📊 Quick Experiment Templates

### Create Reports Directory

```python
from pathlib import Path

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
print(f"Created {reports_dir}")
```

### Save Analysis Results

```python
import pandas as pd

# Save DataFrame
df.to_csv("reports/analysis_results.csv", index=False)

# Save plot
import matplotlib.pyplot as plt
fig.savefig("reports/analysis_plot.png", dpi=150, bbox_inches='tight')
plt.close(fig)
```

---

## � Maintenance Checklist

- [ ] Run `pytest` after major library changes.
- [ ] Trim large notebook outputs before committing (keep figures but avoid raw arrays).
- [ ] Update `SESSION_STATE.md` and `PROJECT_STATUS.md` after each focused work session.
- [ ] Ensure new CSV/plot artifacts land under `reports/` with descriptive filenames.

---

## � Reference Map

| Goal                     | Resource                                                     |
| ------------------------ | ------------------------------------------------------------ |
| Core API usage           | `README.md`                                                  |
| Batch framework          | `BATCH_PROCESSING.md`                                        |
| Implementation internals | `BATCH_IMPLEMENTATION.md`                                    |
| Daily continuity         | `SESSION_STATE.md`                                           |
| Current status           | `PROJECT_STATUS.md`                                          |
| Latest experiments       | `examples/dolphin_communication_analysis.ipynb` & `reports/` |

---

## ✅ Definition of “Ready for Whistle Work”

- [ ] Click detection tuned with acceptable false-positive rate across buoy + special files.
- [ ] Chunk-level statistics summarized for at least 5 representative recordings.
- [ ] Documentation updated with findings and next questions.

Once these boxes are checked, dive into whistle detection and begin cataloging contour metadata.

---

**Stay methodical:** small, reproducible experiments with saved artifacts keep the project nimble and ready for the next wave of ideas.
