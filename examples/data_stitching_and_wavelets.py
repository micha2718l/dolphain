"""
Data Stitching and Wavelet Analysis Demo

This script demonstrates:
1. Loading the built-in catalog
2. Stitching data across multiple file boundaries
3. Visualizing wavelet decomposition
4. Saving audio as WAV files

These capabilities make it easy to:
- Access data by time range without worrying about file boundaries
- Understand how wavelet denoising works
- Export audio for playback or further analysis
"""

import dolphain
from dolphain.catalog import Catalog
import datetime
import matplotlib.pyplot as plt

print("=" * 80)
print("Dolphain: Data Stitching and Wavelet Analysis Demo")
print("=" * 80)
print()

# ============================================================================
# 1. Load Built-in Catalog
# ============================================================================
print("Step 1: Loading built-in catalog...")
catalog = Catalog()
print(f"  ✓ Loaded {len(catalog.df)} files")
print(
    f"  Time range: {catalog.df['start_time'].min()} to {catalog.df['end_time'].max()}"
)
print()

# ============================================================================
# 2. Query and Fetch Data Across File Boundaries
# ============================================================================
print("Step 2: Fetching data that spans multiple files...")

# Select a time range from the middle of the catalog
file_idx = 500
start_file_time = catalog.df.iloc[file_idx]["start_time"]
start_time = start_file_time + datetime.timedelta(seconds=235)
duration = 90  # seconds

print(f"  Requesting {duration}s starting at {start_time}")

# Query catalog to see which files will be accessed
end_time = start_time + datetime.timedelta(seconds=duration)
files_needed = catalog.query(start_time, end_time)
print(f"  Catalog query: {len(files_needed)} files needed")

# Fetch the stitched data
audio_data = dolphain.getData("GoMRI-17", start_time, duration)
print(f"  ✓ Retrieved {len(audio_data):,} samples ({duration}s at 192 kHz)")
print()

# ============================================================================
# 3. Save Audio as WAV
# ============================================================================
print("Step 3: Saving stitched audio as WAV...")
output_wav = "stitched_dolphins.wav"
dolphain.save_wav(audio_data, output_wav)
print()

# ============================================================================
# 4. Visualize Wavelet Decomposition
# ============================================================================
print("Step 4: Visualizing wavelet decomposition...")
print("  This shows how the signal is broken down into frequency bands")
print("  Each level represents approximately half the frequency of the level above")
print()

# Plot decomposition of a subset for clarity
dolphain.plot_wavelet_decomposition(
    audio_data,
    duration=10,  # Plot first 10 seconds
    start_offset=10,  # Start at 10 seconds into the data
    wavelet="db20",
    level=5,
)

# ============================================================================
# 5. Visualize Waveform and Spectrogram
# ============================================================================
print("\nStep 5: Creating waveform and spectrogram...")

import numpy as np

time = np.linspace(0, duration, len(audio_data))

fig, axes = plt.subplots(2, 1, figsize=(14, 8))

# Waveform
axes[0].plot(time, audio_data, linewidth=0.5, color="steelblue")
axes[0].set_title(f"Stitched Waveform - {duration}s from {len(files_needed)} files")
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Amplitude")
axes[0].grid(True, alpha=0.3)

# Spectrogram
axes[1].specgram(audio_data, Fs=192000, NFFT=1024, noverlap=512, cmap="nipy_spectral")
axes[1].set_title("Spectrogram")
axes[1].set_ylabel("Frequency (Hz)")
axes[1].set_xlabel("Time (s)")

plt.tight_layout()
plt.show()

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 80)
print("Summary")
print("=" * 80)
print(f"✓ Loaded built-in catalog: {len(catalog.df)} files")
print(f"✓ Stitched {duration}s of audio from {len(files_needed)} separate files")
print(f"✓ Saved audio to: {output_wav}")
print(f"✓ Visualized wavelet decomposition (5 levels, db20 wavelet)")
print(f"✓ Created waveform and spectrogram visualizations")
print()
print("Key Features Demonstrated:")
print("  • Time-based data access (no need to manage individual files)")
print("  • Seamless stitching across file boundaries")
print("  • Wavelet decomposition visualization")
print("  • Audio export for playback or further analysis")
print("=" * 80)
