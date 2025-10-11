# Next Steps – October 2025 Roadmap

The Dolphain library is stable; we’re now building higher-level analyses for dolphin communication. Use this guide to pick up the next piece of work quickly.

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

### Chunk Summary Logging

```python
chunk_stats = []
for start, end, chunk in iterate_chunks(data, sample_rate, chunk_duration=5.0):
    times, _, amps = detect_clicks(chunk, sample_rate, threshold_factor=6.0)
    chunk_stats.append({
        "start_s": start / sample_rate,
        "click_rate_per_s": len(times) / 5.0,
        "median_amp": np.median(amps) if len(amps) else np.nan,
    })

chunk_df = pd.DataFrame(chunk_stats)
chunk_df.to_csv("reports/chunk_scan_threshold6.csv", index=False)
```

### Whistle Detection Skeleton

```python
from scipy.signal import butter, filtfilt

def detect_whistles(signal_array, fs, band=(2000, 20000), min_duration=0.1):
    b, a = butter(4, np.array(band) / (fs / 2), btype="bandpass")
    filtered = filtfilt(b, a, signal_array)
    # TODO: generate spectrogram, extract ridges, build contour metadata
    raise NotImplementedError
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
