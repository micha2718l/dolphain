#!/usr/bin/env python3
"""Generate example visualizations for the Dolphain landing page."""

import dolphain
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# Create site/images directory
import os
os.makedirs('site/images', exist_ok=True)

# Select a sample file
sample_file = 'data/Buoy210_100300_100399/718587E0.210'

print(f"Reading file: {sample_file}")
data = dolphain.read_ears_file(sample_file)

print(f"Sample rate: {data['fs']} Hz")
print(f"Duration: {data['duration']:.2f} seconds")
print(f"Samples: {data['n_samples']}")

# 1. Waveform visualization
print("\n1. Creating waveform plot...")
fig, ax = plt.subplots(figsize=(12, 4), dpi=100)
time = np.arange(len(data['data'])) / data['fs']
ax.plot(time, data['data'], linewidth=0.5, color='#178ca4')
ax.set_xlabel('Time (seconds)', fontsize=12)
ax.set_ylabel('Amplitude', fontsize=12)
ax.set_title('Underwater Acoustic Recording - Gulf of Mexico', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_facecolor('#f5f5f5')
fig.tight_layout()
plt.savefig('site/images/waveform.png', bbox_inches='tight', facecolor='white')
plt.close()
print("   ✓ Saved: site/images/waveform.png")

# 2. Spectrogram
print("\n2. Creating spectrogram...")
fig, ax = plt.subplots(figsize=(12, 6), dpi=100)
# Use smaller window for better frequency resolution
nfft = 2048
noverlap = nfft // 2
spec, freqs, times, im = ax.specgram(
    data['data'], 
    NFFT=nfft,
    Fs=data['fs'],
    noverlap=noverlap,
    cmap='viridis',
    scale='dB',
    mode='psd'
)
ax.set_ylim(0, 50000)  # Focus on 0-50 kHz
ax.set_xlabel('Time (seconds)', fontsize=12)
ax.set_ylabel('Frequency (Hz)', fontsize=12)
ax.set_title('Spectrogram: Dolphin Clicks and Whistles', fontsize=14, fontweight='bold')
cbar = plt.colorbar(im, ax=ax, label='Power (dB)')
fig.tight_layout()
plt.savefig('site/images/spectrogram.png', bbox_inches='tight', facecolor='white')
plt.close()
print("   ✓ Saved: site/images/spectrogram.png")

# 3. Denoising comparison
print("\n3. Creating denoising comparison...")
# Use a small segment for clarity
segment_duration = 0.5  # seconds
segment_samples = int(segment_duration * data['fs'])
segment = data['data'][:segment_samples]

# Denoise
denoised = dolphain.wavelet_denoise(segment)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6), dpi=100)
time_seg = np.arange(len(segment)) / data['fs']

# Original
ax1.plot(time_seg, segment, linewidth=0.8, color='#ff6b6b', alpha=0.7)
ax1.set_ylabel('Amplitude', fontsize=11)
ax1.set_title('Original Signal (with noise)', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_facecolor('#f5f5f5')

# Denoised
ax2.plot(time_seg, denoised, linewidth=0.8, color='#2d5f3f')
ax2.set_xlabel('Time (seconds)', fontsize=11)
ax2.set_ylabel('Amplitude', fontsize=11)
ax2.set_title('Denoised Signal (wavelet filtering)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_facecolor('#f5f5f5')

fig.tight_layout()
plt.savefig('site/images/denoising.png', bbox_inches='tight', facecolor='white')
plt.close()
print("   ✓ Saved: site/images/denoising.png")

print("\n✅ All example visualizations created successfully!")
print(f"\nSummary:")
print(f"  - Waveform: Full recording ({data['duration']:.2f}s)")
print(f"  - Spectrogram: 0-50 kHz frequency range showing dolphin communication bands")
print(f"  - Denoising: First {segment_duration}s showing wavelet filtering effectiveness")

