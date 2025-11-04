#!/usr/bin/env python3
"""
Quick Start: HuggingFace EARS Integration

This example demonstrates the super easy way to load and analyze
EARS files from HuggingFace using dolphain.

Requirements:
    pip install huggingface_hub
"""

import dolphain

# ============================================================================
# Method 1: The Easiest Way - Random File
# ============================================================================
print("=" * 70)
print("Method 1: Load a random file from HuggingFace")
print("=" * 70)

# Just one line! This fetches a random file and loads it
ears = dolphain.EARS()

# See what you got
print(ears)
print()

# Get detailed info
ears.info()
print()


# ============================================================================
# Method 2: Specific File
# ============================================================================
print("\n" + "=" * 70)
print("Method 2: Load a specific file")
print("=" * 70)

# Load a specific file by name
ears_specific = dolphain.EARS(filename="7178E5DC.200")
print(ears_specific)
print()


# ============================================================================
# Method 3: Different Buoy
# ============================================================================
print("\n" + "=" * 70)
print("Method 3: Load from a different buoy")
print("=" * 70)

# Get a file from BUOY210 instead of default BUOY200
ears_buoy210 = dolphain.EARS(data_path="2017_South/BUOY210")
print(ears_buoy210)
print()


# ============================================================================
# Using the Data
# ============================================================================
print("\n" + "=" * 70)
print("Working with the data")
print("=" * 70)

# Access the audio data directly
print(f"Audio data shape: {ears.data.shape}")
print(f"Sampling rate: {ears.fs} Hz")
print(f"Duration: {ears.duration:.2f} seconds")
print()

# Apply wavelet denoising
print("Applying wavelet denoising...")
denoised = ears.denoise(wavelet='db20')
print(f"✓ Denoised data shape: {denoised.shape}")
print()

# Detect dolphin whistles
print("Detecting whistles...")
whistles = ears.detect_whistles(freq_range=(2000, 20000), min_duration=0.1)
print(f"✓ Found {len(whistles)} whistles")
if whistles:
    w = whistles[0]
    print(f"  First whistle: {w['start_time']:.2f}s - {w['end_time']:.2f}s, "
          f"{w['min_freq']:.0f}-{w['max_freq']:.0f} Hz")
print()


# ============================================================================
# Visualization
# ============================================================================
print("\n" + "=" * 70)
print("Creating visualizations")
print("=" * 70)

# Plot overview
print("Generating overview plot...")
ears.plot('overview', fmax=50000)

# Plot with denoising comparison
print("Generating denoising comparison...")
ears.plot('denoising', wavelet='db20', fmax=50000, xlim=(0, 10))

# Plot spectrogram only
print("Generating spectrogram...")
ears.plot('spectrogram', fmax=25000, figsize=(16, 6))

print("\n✓ All visualizations complete!")


# ============================================================================
# Alternative: Use the Function Directly
# ============================================================================
print("\n" + "=" * 70)
print("Alternative: Using fetch_huggingface_file() function")
print("=" * 70)

# If you prefer to work with dictionaries instead of class instances
data = dolphain.fetch_huggingface_file()
print(f"Loaded: {data['filename']}")
print(f"Duration: {data['duration']:.2f}s")
print(f"Data shape: {data['data'].shape}")
print(f"Source: {data['source']}")

# Then use it with plotting functions
dolphain.plot_waveform(data, figsize=(16, 6))


# ============================================================================
# Pro Tips
# ============================================================================
print("\n" + "=" * 70)
print("💡 Pro Tips")
print("=" * 70)
print("""
1. Keep temp files for inspection:
   ears = dolphain.EARS(cleanup=False)
   print(f"File saved at: {ears.metadata['temp_path']}")

2. Load from local file:
   ears = dolphain.EARS('path/to/local/file.200')

3. Chain operations:
   whistles = dolphain.EARS().detect_whistles()

4. Access full metadata:
   print(ears.metadata.keys())

5. Combine with batch processing:
   for i in range(5):
       ears = dolphain.EARS()
       whistles = ears.detect_whistles()
       print(f"{ears.filename}: {len(whistles)} whistles")
""")

print("=" * 70)
print("🎉 Complete! Happy analyzing!")
print("=" * 70)
