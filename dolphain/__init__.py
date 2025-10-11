"""
Dolphain - Underwater Acoustic Data Analysis

A Python package for reading and analyzing EARS (Ecological Acoustic Recorder)
binary data files from underwater acoustic recordings in the Gulf of Mexico.
"""

__version__ = "0.1.0"
__author__ = "Michael Haas"

# Import all public functions from submodules
from .io import read_ears_file, print_file_info
from .signal import wavelet_denoise, threshold, thresh_wave_coeffs, detect_whistles
from .plotting import (
    plot_waveform,
    plot_spectrogram,
    plot_overview,
    plot_denoising_comparison,
    plot_wavelet_comparison,
)
from .batch import (
    find_data_files,
    select_random_files,
    BatchProcessor,
    ResultCollector,
    timer,
)

# Define public API
__all__ = [
    # I/O functions
    "read_ears_file",
    "print_file_info",
    # Signal processing
    "wavelet_denoise",
    "threshold",
    "thresh_wave_coeffs",
    "detect_whistles",
    # Plotting
    "plot_waveform",
    "plot_spectrogram",
    "plot_overview",
    "plot_denoising_comparison",
    "plot_wavelet_comparison",
    # Batch processing
    "find_data_files",
    "select_random_files",
    "BatchProcessor",
    "ResultCollector",
    "timer",
]
