# 🚀 START HERE - Dolphain Project

**Last Updated:** December 13, 2025
**Status:** ✅ **PRODUCTION READY** - Modern modular showcase deployed

---

## 🎯 What Is Dolphain?

**Mission:** Analyze 949,504 underwater acoustic recordings to detect and understand dolphin communication patterns.

**Innovation:** 6-feature "interestingness" scoring system beyond simple whistle counting:
- Activity level (RMS energy)
- Spectral diversity (frequency range)
- Signal-to-noise ratio
- Complexity (zero-crossings)
- Temporal patterns (autocorrelation)
- Overlapping signals

**Output:** Interactive web showcase with professional audio players, spectrograms, and waveforms.

---

## ⚡ Quick Start

### 1. View the Showcase Locally

```bash
cd site
python3 -m http.server 8000
# Open http://localhost:8000/showcase.html
```

### 2. Analyze Data with Python

```python
import dolphain
ears = dolphain.EARS() # Loads random file from HuggingFace
ears.plot('spectrogram')
```

### 3. Access Data by Time (New!)

```python
from dolphain import getData, build_catalog
import datetime

# build_catalog() # Run once
data = getData("GoMRI-17", datetime.datetime(2017, 6, 28, 0, 20, 51), 10.0)
```

---

## 📚 Documentation

- **[README.md](README.md)**: Full API documentation
- **[DATA_ACCESS.md](DATA_ACCESS.md)**: Guide to time-based data access
- **[DOC_INDEX.md](DOC_INDEX.md)**: Index of all documentation files

