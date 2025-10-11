#!/usr/bin/env python3
"""
Quick test of batch processing functionality.
"""

import sys

sys.path.insert(0, ".")

import dolphain
import numpy as np


def simple_pipeline(filepath):
    """Simple test pipeline."""
    data = dolphain.read_ears_file(filepath)
    return {
        "duration": data["duration"],
        "rms": np.sqrt(np.mean(data["data"] ** 2)),
        "peak": np.max(np.abs(data["data"])),
    }


print("Finding data files...")
files = dolphain.find_data_files("data", "**/*.210")
print(f"Found {len(files)} total files")

print("\nSelecting random subset...")
subset = dolphain.select_random_files(files, n=3, seed=42)
print(f"Selected {len(subset)} files")

print("\nRunning batch processing...")
processor = dolphain.BatchProcessor(verbose=True)
collector = processor.process_files(subset, simple_pipeline)

print("\nPrinting summary...")
collector.print_summary()

print("\n✓ Batch processing test complete!")
