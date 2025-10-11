#!/usr/bin/env python3
"""
Test script to verify dolphain package is working correctly.

Run this to verify your installation:
    python test_ears_reader.py
"""

import sys
from pathlib import Path

# Add parent directory to path for development testing
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy import signal
        import pywt
        import dolphain

        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_read_file():
    """Test reading a sample EARS file."""
    print("\nTesting file reading...")
    try:
        import dolphain

        # Try to find a sample file
        sample_files = [
            Path("../unophysics/sample_data/71621DC7.190"),
            Path("../fourier_examples/data/7164403B.130"),
            Path("unophysics/sample_data/71621DC7.190"),
            Path("fourier_examples/data/7164403B.130"),
        ]

        test_file = None
        for f in sample_files:
            if f.exists():
                test_file = f
                break

        if test_file is None:
            print("⚠ No sample files found to test")
            return None

        data = dolphain.read_ears_file(test_file)

        # Verify data structure
        required_keys = [
            "data",
            "fs",
            "time_start",
            "time_end",
            "timestamps",
            "duration",
            "n_samples",
        ]
        for key in required_keys:
            if key not in data:
                print(f"✗ Missing key in data: {key}")
                return False

        print(f"✓ Successfully read file: {test_file}")
        print(f"  Duration: {data['duration']:.2f} seconds")
        print(f"  Samples: {data['n_samples']:,}")
        print(f"  Sampling rate: {data['fs']:,} Hz")
        return True

    except Exception as e:
        print(f"✗ File reading failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_functions():
    """Test that all module functions are available."""
    print("\nTesting module functions...")
    try:
        import dolphain

        functions = [
            # I/O functions
            "read_ears_file",
            "print_file_info",
            # Signal processing
            "wavelet_denoise",
            "threshold",
            "thresh_wave_coeffs",
            # Plotting
            "plot_waveform",
            "plot_spectrogram",
            "plot_overview",
            "plot_denoising_comparison",
            "plot_wavelet_comparison",
        ]

        for func_name in functions:
            if not hasattr(dolphain, func_name):
                print(f"✗ Function missing: {func_name}")
                return False
            if not callable(getattr(dolphain, func_name)):
                print(f"✗ Not callable: {func_name}")
                return False

        print(f"✓ All {len(functions)} functions available and callable")
        return True

    except Exception as e:
        print(f"✗ Function test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("Dolphain Package Test")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Import test", test_imports()))
    results.append(("Function test", test_functions()))
    results.append(("File reading test", test_read_file()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)
    skipped = sum(1 for _, result in results if result is None)

    for test_name, result in results:
        status = (
            "✓ PASS" if result is True else ("⚠ SKIP" if result is None else "✗ FAIL")
        )
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed} passed, {failed} failed, {skipped} skipped")

    if failed > 0:
        print("\n⚠ Some tests failed. Check your installation.")
        return 1
    elif passed > 0:
        print("\n✓ All tests passed! Module is working correctly.")
        return 0
    else:
        print("\n⚠ No tests could be run.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
