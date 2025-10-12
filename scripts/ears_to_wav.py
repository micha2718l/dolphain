#!/usr/bin/env python3
"""
Convert EARS file to WAV for listening.

Creates two WAV files:
- _raw.wav (original signal)
- _denoised.wav (after wavelet denoising)

Usage:
    python ears_to_wav.py 72146FB7.171
    python ears_to_wav.py /path/to/file.210
"""

import sys
import argparse
from pathlib import Path
import numpy as np
from scipy.io import wavfile

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


def ears_to_wav(ears_file: Path, output_dir: Path = None, normalize: bool = True):
    """
    Convert EARS file to WAV files (raw and denoised).
    
    Args:
        ears_file: Path to EARS file
        output_dir: Where to save WAV files (default: current directory)
        normalize: Normalize to prevent clipping (default: True)
    """
    output_dir = output_dir or Path.cwd()
    output_dir.mkdir(exist_ok=True)
    
    # Find the file if just filename given
    if not ears_file.exists():
        print(f"Searching for file: {ears_file.name}")
        # Try to find in file list
        file_list = Path("ears_files_list.txt")
        if file_list.exists():
            with open(file_list, 'r') as f:
                for line in f:
                    if ears_file.name in line:
                        ears_file = Path(line.strip())
                        print(f"Found: {ears_file}")
                        break
    
    if not ears_file.exists():
        print(f"❌ File not found: {ears_file}")
        return False
    
    print(f"\n{'='*80}")
    print(f"Converting: {ears_file.name}")
    print(f"{'='*80}\n")
    
    # Read EARS file
    print("Reading EARS file...")
    data = dolphain.read_ears_file(ears_file)
    signal = data['data']
    fs = data['fs']
    duration = data['duration']
    
    print(f"  Duration: {duration:.2f}s")
    print(f"  Sample rate: {fs} Hz")
    print(f"  Samples: {len(signal)}")
    print(f"  Range: [{signal.min():.6f}, {signal.max():.6f}]")
    
    # Denoise
    print("\nDenoising signal...")
    signal_clean = dolphain.wavelet_denoise(signal, wavelet='db8')
    
    # Normalize to 16-bit range if requested
    if normalize:
        print("Normalizing signals...")
        # Scale to use most of 16-bit range without clipping
        max_val = max(abs(signal.min()), abs(signal.max()))
        signal_norm = (signal / max_val * 32767 * 0.95).astype(np.int16)
        
        max_val_clean = max(abs(signal_clean.min()), abs(signal_clean.max()))
        signal_clean_norm = (signal_clean / max_val_clean * 32767 * 0.95).astype(np.int16)
    else:
        # Just convert to 16-bit
        signal_norm = (signal * 32767).astype(np.int16)
        signal_clean_norm = (signal_clean * 32767).astype(np.int16)
    
    # Save WAV files
    base_name = ears_file.stem
    
    raw_path = output_dir / f"{base_name}_raw.wav"
    clean_path = output_dir / f"{base_name}_denoised.wav"
    
    print(f"\nSaving WAV files...")
    wavfile.write(raw_path, fs, signal_norm)
    print(f"  ✓ Raw: {raw_path}")
    
    wavfile.write(clean_path, fs, signal_clean_norm)
    print(f"  ✓ Denoised: {clean_path}")
    
    print(f"\n{'='*80}")
    print("✅ COMPLETE!")
    print(f"{'='*80}")
    print(f"\nYou can now listen to:")
    print(f"  {raw_path.name}")
    print(f"  {clean_path.name}")
    
    # File sizes
    raw_size = raw_path.stat().st_size / (1024*1024)
    clean_size = clean_path.stat().st_size / (1024*1024)
    print(f"\nFile sizes:")
    print(f"  Raw: {raw_size:.2f} MB")
    print(f"  Denoised: {clean_size:.2f} MB")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Convert EARS file to WAV for listening',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert by filename (searches in file list)
  python ears_to_wav.py 72146FB7.171
  
  # Convert by full path
  python ears_to_wav.py /Volumes/ladcuno8tb0/2017_West/Buoy171/72146FB7.171
  
  # Save to specific directory
  python ears_to_wav.py 72146FB7.171 --output-dir audio_files/
  
  # Don't normalize (keep original amplitudes)
  python ears_to_wav.py 72146FB7.171 --no-normalize
        """
    )
    
    parser.add_argument('ears_file', type=Path,
                       help='EARS file to convert (filename or full path)')
    parser.add_argument('--output-dir', type=Path,
                       help='Output directory (default: current directory)')
    parser.add_argument('--no-normalize', action='store_true',
                       help='Do not normalize amplitude')
    
    args = parser.parse_args()
    
    success = ears_to_wav(
        args.ears_file,
        output_dir=args.output_dir,
        normalize=not args.no_normalize
    )
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
