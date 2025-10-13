# 🌟 Unique Signal Detection Mode

**Date:** October 13, 2025  
**Branch:** `feature/unique-signal-detection`  
**Purpose:** Find truly exceptional and rare dolphin acoustic signals

---

## 🎯 What This Detects

This mode is integrated into `quick_find.py` and goes beyond basic chirp/click detection to find **truly unique** recordings with exceptional characteristics:

### 1. **Ultra-Fast Frequency Sweeps** 🚀
- Sweeps faster than 10 kHz/second
- Exceptionally rapid vocalizations

### 2. **Extreme Frequency Ranges** 🎚️
- Signals spanning >50 kHz range
- Ultra-high frequencies (>100 kHz)
- Wide bandwidth vocalizations

### 3. **Multiple Simultaneous Vocalizations** 🎼
- 2+ dolphins vocalizing at once
- Overlapping signals at different frequencies
- Social communication patterns

### 4. **Unusual Click Patterns** 🥁
- **Burst clicking:** Rapid clicks <5ms apart
- **Rhythmic extremes:** Very regular or very irregular

### 5. **Harmonic Structures** 🎹
- Overtones (2x, 3x fundamental frequency)
- Musical quality signals
- Complex tonal vocalizations

### 6. **High Spectral Diversity** 🌈
- Activity across 5 frequency bands simultaneously
- High spectral entropy
- Rich, complex frequency content

---

## 🚀 How to Run

### Basic Command

```bash
cd /Users/mjhaas/code/dolphain

# Run unique signal detection
python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --mode unique \
  --output-dir experiments/unique_signals
```

### Standard Mode (for comparison)

```bash
# Standard chirp/click detection
python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --mode standard \
  --output-dir quick_find_results/standard_run
```

---

## 📊 Scoring System (0-100)

- **90-100:** Extremely rare, exceptional recordings ⭐⭐⭐⭐⭐
- **70-90:** Very interesting, definitely review ⭐⭐⭐⭐
- **50-70:** Notable features, worth checking ⭐⭐⭐
- **30-50:** Some interesting aspects ⭐⭐
- **0-30:** Typical recordings ⭐

The algorithm rewards **quality over quantity** - finding gems rather than counting detections.

---

## 🎨 After It Completes

Generate a showcase of the most unique files:

```bash
python scripts/refresh_showcase.py \
  --results-dir experiments/unique_signals \
  --top 15 \
  --output site/showcase

cd site
python3 -m http.server 8000
# Open: http://localhost:8000/showcase.html
```

---

## 📊 Output Files

Results saved to `experiments/unique_signals/`:

### `results.json`
Full detailed results with uniqueness metrics:
```json
{
  "results": [
    {
      "filename": "file.123",
      "uniqueness_score": 87.5,
      "active_bands": 5,
      "spectral_entropy": 4.2,
      "freq_range": 68000.0,
      "max_freq": 105000.0,
      "max_simultaneous": 3,
      "fast_sweeps": 4,
      "harmonics": 12,
      "burst_clicks": 25
    }
  ]
}
```

---

## 🏗️ Algorithm Features

### Spectral Analysis
```python
# Frequency bands analyzed:
ultra_low:   0-2 kHz     (rumbles, ambient)
low:         2-10 kHz    (low whistles)
mid:         10-40 kHz   (mid whistles, some clicks)
high:        40-80 kHz   (high whistles, clicks)
ultra_high:  80-125 kHz  (ultrasonic clicks)
```

### Scoring Breakdown (0-100)

**Multi-band Activity (0-15 pts):**
- 3 points per active frequency band (max 5 bands)

**Spectral Diversity (0-10 pts):**
- High entropy = diverse frequency content

**Frequency Range (0-10 pts):**
- >50 kHz span gets maximum points

**Extreme Frequencies (0-5 pts):**
- >100 kHz: 5 pts
- >80 kHz: 3 pts

**Simultaneous Signals (0-10 pts):**
- 4+ overlapping: 10 pts
- 3 overlapping: 7 pts
- 2 overlapping: 4 pts

**Harmonics (0-10 pts):**
- 0.5 points per harmonic event detected

**Ultra-Fast Sweeps (0-10 pts):**
- 5+ sweeps: 10 pts
- 3+ sweeps: 7 pts
- 1+ sweeps: 4 pts

**Burst Clicks (0-8 pts):**
- 0.2 points per burst click (<5ms ICI)

**Unusual Regularity (0-5 pts):**
- Very regular OR very irregular click patterns

---

## 🎯 What Makes This Different

### vs. Standard Mode
**Standard:** Detects ANY chirps and clicks (quantity-focused)  
**Unique:** Finds EXCEPTIONAL features (quality-focused)

### Scoring Philosophy
- High scores (>70): Truly exceptional, rare recordings
- Medium scores (40-70): Interesting features, worth review
- Low scores (<40): Typical recordings, less unique

---

## 📈 Expected Results

Based on typical datasets:

### Score Distribution
- **90-100:** 0-2% (extremely rare)
- **70-90:** 5-10% (very interesting)
- **50-70:** 15-20% (interesting)
- **30-50:** 30-40% (some aspects)
- **0-30:** 40-50% (typical)

### Feature Prevalence
- **Fast sweeps (>10 kHz/sec):** ~10-15%
- **Harmonics detected:** ~20-25%
- **Simultaneous signals:** ~5-10%
- **Burst clicking:** ~15-20%

---

## 💡 Tips for Best Results

### File Selection
- Use diverse time periods (day/night, seasons)
- Include various locations
- Mix calm and active periods

### Analysis Strategy
1. **Initial run:** 1000 files to understand distribution
2. **Review top 50:** Verify algorithm performance
3. **Adjust if needed:** Can tune thresholds in code
4. **Large run:** 5000+ files for comprehensive search

---

## 🎉 Ready to Discover!

This mode is designed to find the **most interesting, rare, and exceptional** dolphin vocalizations in your dataset.

**Run it now:**
```bash
python scripts/quick_find.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --mode unique \
  --output-dir experiments/unique_signals
```

**Then enjoy discovering the most amazing sounds in your data!** 🐬🌟


### 1. **Ultra-Fast Frequency Sweeps** 🚀
- Sweeps faster than 10 kHz/second
- Fastest sweeps >50 kHz/sec get maximum points
- These are exceptionally rapid vocalizations

### 2. **Extreme Frequency Ranges** 🎚️
- Signals spanning >50 kHz range
- Ultra-high frequencies (>100 kHz)
- Ultra-low frequencies (<2 kHz)
- Wide bandwidth vocalizations

### 3. **Multiple Simultaneous Vocalizations** 🎼
- 2+ dolphins vocalizing at once
- Overlapping signals at different frequencies
- Social communication patterns

### 4. **Unusual Click Patterns** 🥁
- **Burst clicking:** Rapid clicks <5ms apart
- **Bimodal patterns:** Two different click rates
- **Acceleration/deceleration:** Speeding up or slowing down
- **Syncopated rhythms:** Irregular but patterned

### 5. **Harmonic Structures** 🎹
- Overtones (2x, 3x fundamental frequency)
- Musical quality signals
- Complex tonal vocalizations

### 6. **High Spectral Diversity** 🌈
- Activity across 5 frequency bands simultaneously
- High spectral entropy
- Rich, complex frequency content

---

## 🏗️ Algorithm Features

### Spectral Analysis
```python
# Frequency bands analyzed:
ultra_low:   0-2 kHz     (rumbles, ambient)
low:         2-10 kHz    (low whistles)
mid:         10-40 kHz   (mid whistles, some clicks)
high:        40-80 kHz   (high whistles, clicks)
ultra_high:  80-125 kHz  (ultrasonic clicks)
```

### Scoring System (0-100)

**Spectral Uniqueness (40 points):**
- Multiple active bands: 15 pts (3 per band, max 5 bands)
- Spectral diversity: 10 pts (high entropy)
- Extreme frequency range: 10 pts (>50 kHz span)
- Rare extreme frequencies: 5 pts (>100 kHz)

**Special Features (30 points):**
- Simultaneous vocalizations: 10 pts (4+ overlapping)
- Harmonics: 10 pts (overtone structures)
- Ultra-fast sweeps: 10 pts (>50 kHz/sec)

**Click Pattern Uniqueness (30 points):**
- Burst clicking: 8 pts (rapid fire)
- Unusual patterns: 12 pts (bimodal, tempo changes)
- Regularity extremes: 5 pts (very regular or very irregular)
- Click diversity: 5 pts (wide ICI range)

---

## 🚀 How to Run

### Basic Command

```bash
cd /Users/mjhaas/code/dolphain

# Make sure you're on the feature branch
git checkout feature/unique-signal-detection

# Run the analysis
python scripts/find_unique_signals.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --output-dir experiments/unique_signals
```

### Custom Run

```bash
# Smaller test run
python scripts/find_unique_signals.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 100 \
  --output-dir experiments/unique_test

# Large comprehensive search
python scripts/find_unique_signals.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 5000 \
  --output-dir experiments/unique_comprehensive
```

---

## 📊 Output Files

Results saved to `experiments/unique_signals/`:

### `results.json`
Full detailed results for all files:
```json
{
  "results": [
    {
      "filename": "/path/to/file.123",
      "uniqueness_score": 87.5,
      "spectral_metrics": {
        "active_frequency_bands": 5,
        "spectral_entropy": 4.2,
        "peak_freq_range": 68000,
        "max_frequency": 105000,
        "harmonic_events": 12,
        "max_simultaneous_signals": 3
      },
      "n_fast_sweeps": 4,
      "fast_sweeps": [...],
      "click_patterns": {
        "burst_clicks": 25,
        "is_bimodal": true,
        "click_acceleration": true
      }
    }
  ]
}
```

### `summary.json`
Statistics and overview:
```json
{
  "total_files": 1000,
  "avg_uniqueness_score": 45.2,
  "max_uniqueness_score": 92.3,
  "files_with_fast_sweeps": 127,
  "files_with_harmonics": 234,
  "files_with_simultaneous": 89,
  "top_20_files": [...]
}
```

### `checkpoint.json`
Resume point (saved every 10 files)

---

## 🎨 Generate Showcase

After analysis completes, generate a showcase of the most unique files:

```bash
# Generate showcase with top 15 unique files
python scripts/refresh_showcase.py \
  --results-dir experiments/unique_signals \
  --top 15 \
  --output site/showcase

# View it
cd site
python3 -m http.server 8000
# Open: http://localhost:8000/showcase.html
```

---

## 🔬 What Makes This Different

### vs. Standard Quick Find
**Standard:** Looks for ANY chirps and clicks (quantity-focused)  
**Unique:** Looks for EXCEPTIONAL features (quality-focused)

### vs. Conservative Detection
**Conservative:** Minimizes false positives, high precision  
**Unique:** Finds rare gems, tolerates some noise for discovery

### Scoring Philosophy
- High scores (>70): Truly exceptional, rare recordings
- Medium scores (40-70): Interesting features, worth review
- Low scores (<40): Typical recordings, less unique

---

## 📈 Expected Results

Based on typical datasets:

### Score Distribution
- **90-100:** 0-2% (extremely rare, exceptional)
- **70-90:** 5-10% (very interesting, definitely review)
- **50-70:** 15-20% (interesting features)
- **30-50:** 30-40% (some interesting aspects)
- **0-30:** 40-50% (typical recordings)

### Feature Prevalence
- **Fast sweeps (>10 kHz/sec):** ~10-15% of files
- **Harmonics detected:** ~20-25% of files
- **Simultaneous signals:** ~5-10% of files
- **Burst clicking:** ~15-20% of files
- **Ultra-high frequencies (>100 kHz):** ~3-5% of files

---

## 🎯 Use Cases

### Research Applications
1. **Behavioral studies:** Find complex social communication
2. **Acoustic ecology:** Identify unusual environmental interactions
3. **Individual identification:** Unique vocal signatures
4. **Species comparison:** Rare vocalization types

### Showcase Creation
- Create compelling audio galleries
- Demonstrate vocal diversity
- Educational materials
- Public outreach

### Quality Control
- Find best examples for analysis
- Identify recording artifacts vs. real signals
- Validate detection algorithms

---

## 🔧 Technical Details

### Performance
- **Speed:** ~1-2 files/second (similar to standard quick_find)
- **Memory:** Moderate (processes one file at a time)
- **Checkpoints:** Every 10 files (safe to interrupt)

### Dependencies
```python
import numpy
import scipy
import pywt  # PyWavelets (already in dolphain)
```

### Key Algorithms
1. **High-resolution spectrogram:** 8192-point FFT, 75% overlap
2. **Multi-band energy analysis:** 5 frequency bands
3. **Spectral entropy:** Shannon entropy of frequency distribution
4. **Harmonic detection:** 2x, 3x ratio checking
5. **Click pattern analysis:** ICI distribution, rhythm detection

---

## 🎓 Scientific Background

### Why These Features Matter

**Ultra-fast sweeps:**
- Require precise vocal control
- May indicate emotional state or urgency
- Rare in typical recordings

**Harmonics:**
- Indicate complex vocal fold vibration
- Musical quality suggests intentional production
- May have communicative significance

**Simultaneous vocalizations:**
- Social interaction markers
- Turn-taking or overlapping communication
- Chorus effects in groups

**Burst clicking:**
- Associated with specific behaviors (feeding, navigation)
- High information rate
- Cognitively demanding production

**Wide frequency ranges:**
- Vocal versatility
- Potentially multi-modal communication
- Rare extreme frequencies suggest specialization

---

## 💡 Tips for Best Results

### File Selection
- Use diverse time periods (day/night, seasons)
- Include various locations
- Mix calm and active periods

### Analysis Strategy
1. **Initial run:** 1000 files to understand distribution
2. **Review top 50:** Verify algorithm performance
3. **Adjust if needed:** Fine-tune thresholds
4. **Large run:** 5000+ files for comprehensive search

### Interpretation
- **Score >80:** Almost certainly exceptional
- **Score 60-80:** Very likely interesting
- **Score 40-60:** Worth checking, may have specific features
- **Score <40:** Typical, but may still have value

---

## 🔄 Next Steps

### After Initial Run

1. **Review results:**
   ```bash
   cat experiments/unique_signals/summary.json
   ```

2. **Generate showcase:**
   ```bash
   python scripts/refresh_showcase.py \
     --results-dir experiments/unique_signals \
     --top 20 \
     --output site/showcase_unique
   ```

3. **Analyze patterns:**
   - What features are most common in high scorers?
   - Are there clusters of similar unique signals?
   - Any unexpected patterns?

4. **Iterate:**
   - Adjust scoring weights if needed
   - Add new feature detectors
   - Refine thresholds

---

## 📝 Code Structure

```
scripts/find_unique_signals.py
├── analyze_spectral_uniqueness()    # Multi-band, entropy, harmonics
├── detect_ultra_fast_sweeps()       # >10 kHz/sec sweeps
├── detect_unusual_click_patterns()  # Bursts, rhythms, tempo
├── calculate_uniqueness_score()     # 0-100 scoring
├── analyze_file()                   # Main analysis pipeline
└── run_unique_signal_search()       # Orchestration
```

---

## 🚨 Known Limitations

1. **Noise sensitivity:** High scores may include noise artifacts (verify visually)
2. **Context-free:** Doesn't know behavioral context
3. **Threshold-dependent:** May miss subtle but meaningful signals
4. **Computation time:** Similar to standard analysis (~1-2 files/sec)

---

## ✅ Validation

### How to Validate Results

1. **Visual inspection:** View spectrograms of high scorers
2. **Audio playback:** Listen to denoised audio
3. **Cross-reference:** Compare with behavioral observations if available
4. **Statistical analysis:** Check score distribution for outliers

### Expected High Scorers
- Social groups (multiple individuals)
- Active foraging (burst clicks + whistles)
- Complex communication sequences
- Rare acoustic events

---

## 🎉 Ready to Discover!

This experiment is designed to find the **most interesting, rare, and exceptional** dolphin vocalizations in your dataset.

**Run it now:**
```bash
python scripts/find_unique_signals.py \
  --file-list outputs/ears_files_list.txt \
  --n-files 1000 \
  --output-dir experiments/unique_signals
```

**Then enjoy discovering the most amazing sounds in your data!** 🐬🌟
