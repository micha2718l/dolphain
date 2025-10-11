"""
Plotting functions for acoustic data visualization.

This module provides various plotting capabilities including waveforms,
spectrograms, and wavelet denoising comparisons.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from .signal import wavelet_denoise

__all__ = [
    "plot_waveform",
    "plot_spectrogram",
    "plot_overview",
    "plot_denoising_comparison",
    "plot_wavelet_comparison",
]


def plot_waveform(ears_data, xlim=None, figsize=(16, 6)):
    """
    Plot the acoustic waveform.

    Parameters
    ----------
    ears_data : dict
        Dictionary returned by read_ears_file()
    xlim : tuple, optional
        Time limits (start, end) in seconds
    figsize : tuple, optional
        Figure size (width, height)

    Examples
    --------
    >>> import dolphain
    >>> data = dolphain.read_ears_file('sample.190')
    >>> dolphain.plot_waveform(data)
    >>> dolphain.plot_waveform(data, xlim=(5, 10))  # Zoom to 5-10 seconds
    """
    data = ears_data["data"]
    fs = ears_data["fs"]
    time_start = ears_data["time_start"]
    duration = ears_data["duration"]

    # Create time array
    time = np.linspace(0, duration, len(data))

    # Create plot
    plt.figure(figsize=figsize)
    plt.plot(time, data, linewidth=0.5)
    plt.xlabel("Time [s]", fontsize=12)
    plt.ylabel("Amplitude [arbitrary units]", fontsize=12)
    plt.title(
        f'Acoustic Recording - Start: {time_start.strftime("%Y-%m-%d %H:%M:%S")} UTC - Duration: {duration:.2f} s',
        fontsize=14,
    )
    plt.grid(True, alpha=0.3)

    if xlim is not None:
        plt.xlim(xlim)

    plt.tight_layout()
    plt.show()


def plot_spectrogram(
    ears_data,
    fmax=None,
    nperseg=1024,
    noverlap=512,
    figsize=(16, 6),
    cmap="nipy_spectral",
    vmin=None,
    vmax=None,
):
    """
    Plot a spectrogram of the acoustic data.

    Parameters
    ----------
    ears_data : dict
        Dictionary returned by read_ears_file()
    fmax : float, optional
        Maximum frequency to display (Hz)
    nperseg : int, optional
        Length of each segment for FFT
    noverlap : int, optional
        Number of points to overlap between segments
    figsize : tuple, optional
        Figure size (width, height)
    cmap : str, optional
        Colormap name
    vmin, vmax : float, optional
        Min and max values for color scale (in dB)

    Examples
    --------
    >>> import dolphain
    >>> data = dolphain.read_ears_file('sample.190')
    >>> dolphain.plot_spectrogram(data, fmax=5000)  # Show up to 5 kHz
    """
    data = ears_data["data"]
    fs = ears_data["fs"]
    time_start = ears_data["time_start"]

    # Compute spectrogram
    f, t, Sxx = signal.spectrogram(data, fs=fs, nperseg=nperseg, noverlap=noverlap)

    # Convert to dB
    Sxx_dB = 10 * np.log10(np.abs(Sxx) + 1e-10)

    # Create plot
    plt.figure(figsize=figsize)
    plt.pcolormesh(t, f, Sxx_dB, shading="gouraud", cmap=cmap, vmin=vmin, vmax=vmax)
    plt.colorbar(label="Power/Frequency [dB/Hz]")
    plt.xlabel("Time [s]", fontsize=12)
    plt.ylabel("Frequency [Hz]", fontsize=12)
    plt.title(
        f'Spectrogram - Start: {time_start.strftime("%Y-%m-%d %H:%M:%S")} UTC',
        fontsize=14,
    )

    if fmax is not None:
        plt.ylim([0, fmax])

    plt.tight_layout()
    plt.show()


def plot_overview(ears_data, fmax=None, xlim_zoom=None, figsize=(16, 12)):
    """
    Create a multi-panel overview plot with waveform and spectrogram.

    Parameters
    ----------
    ears_data : dict
        Dictionary returned by read_ears_file()
    fmax : float, optional
        Maximum frequency to display (Hz)
    xlim_zoom : tuple, optional
        Time limits for zoomed waveform (start, end) in seconds
    figsize : tuple, optional
        Figure size (width, height)

    Examples
    --------
    >>> import dolphain
    >>> data = dolphain.read_ears_file('sample.190')
    >>> dolphain.plot_overview(data, fmax=5000, xlim_zoom=(5, 10))
    """
    data = ears_data["data"]
    fs = ears_data["fs"]
    time_start = ears_data["time_start"]
    duration = ears_data["duration"]

    # Create time array
    time = np.linspace(0, duration, len(data))

    # Compute spectrogram
    f, t, Sxx = signal.spectrogram(data, fs=fs, nperseg=1024, noverlap=512)
    Sxx_dB = 10 * np.log10(np.abs(Sxx) + 1e-10)

    # Create subplots
    fig, axes = plt.subplots(3, 1, figsize=figsize)

    # Full waveform
    axes[0].plot(time, data, linewidth=0.5)
    axes[0].set_xlabel("Time [s]", fontsize=11)
    axes[0].set_ylabel("Amplitude", fontsize=11)
    axes[0].set_title(
        f'Full Waveform - {time_start.strftime("%Y-%m-%d %H:%M:%S")} UTC', fontsize=12
    )
    axes[0].grid(True, alpha=0.3)

    # Spectrogram
    im = axes[1].pcolormesh(t, f, Sxx_dB, shading="gouraud", cmap="nipy_spectral")
    axes[1].set_xlabel("Time [s]", fontsize=11)
    axes[1].set_ylabel("Frequency [Hz]", fontsize=11)
    axes[1].set_title("Spectrogram", fontsize=12)
    if fmax is not None:
        axes[1].set_ylim([0, fmax])
    plt.colorbar(im, ax=axes[1], label="Power/Frequency [dB/Hz]")

    # Zoomed waveform
    axes[2].plot(time, data, linewidth=0.5)
    axes[2].set_xlabel("Time [s]", fontsize=11)
    axes[2].set_ylabel("Amplitude", fontsize=11)
    if xlim_zoom is not None:
        axes[2].set_xlim(xlim_zoom)
        axes[2].set_title(
            f"Zoomed Waveform [{xlim_zoom[0]:.2f} - {xlim_zoom[1]:.2f} s]", fontsize=12
        )
    else:
        axes[2].set_title("Waveform (adjust xlim_zoom parameter to zoom)", fontsize=12)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_denoising_comparison(
    ears_data, wavelet="db20", thresh=None, xlim=None, fmax=None, figsize=(16, 10)
):
    """
    Plot comparison between original and wavelet-denoised data.

    Creates a 2x2 subplot showing:
    - Top left: Original waveform
    - Top right: Denoised waveform
    - Bottom left: Original spectrogram
    - Bottom right: Denoised spectrogram

    Parameters
    ----------
    ears_data : dict
        Dictionary returned by read_ears_file()
    wavelet : str, optional
        Wavelet name (default: 'db20')
    thresh : float, optional
        Threshold value. If None, calculated automatically
    xlim : tuple, optional
        Time limits (start, end) in seconds for zooming
    fmax : float, optional
        Maximum frequency for spectrograms (Hz)
    figsize : tuple, optional
        Figure size (width, height)

    Examples
    --------
    >>> import dolphain
    >>> data = dolphain.read_ears_file('sample.190')
    >>> dolphain.plot_denoising_comparison(data)
    >>> dolphain.plot_denoising_comparison(data, wavelet='db8', xlim=(5, 15), fmax=5000)
    """
    data = ears_data["data"]
    fs = ears_data["fs"]
    time_start = ears_data["time_start"]
    duration = ears_data["duration"]

    # Denoise the data
    denoised, threshold_used = wavelet_denoise(
        data, wavelet=wavelet, thresh=thresh, return_threshold=True
    )

    # Create time array
    time = np.linspace(0, duration, len(data))

    # Compute spectrograms
    f_orig, t_orig, Sxx_orig = signal.spectrogram(
        data, fs=fs, nperseg=1024, noverlap=512
    )
    Sxx_orig_dB = 10 * np.log10(np.abs(Sxx_orig) + 1e-10)

    f_clean, t_clean, Sxx_clean = signal.spectrogram(
        denoised, fs=fs, nperseg=1024, noverlap=512
    )
    Sxx_clean_dB = 10 * np.log10(np.abs(Sxx_clean) + 1e-10)

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=figsize)

    # Original waveform
    axes[0, 0].plot(time, data, linewidth=0.5)
    axes[0, 0].set_xlabel("Time [s]", fontsize=11)
    axes[0, 0].set_ylabel("Amplitude", fontsize=11)
    axes[0, 0].set_title("Original Waveform", fontsize=12, fontweight="bold")
    axes[0, 0].grid(True, alpha=0.3)
    if xlim:
        axes[0, 0].set_xlim(xlim)

    # Denoised waveform
    axes[0, 1].plot(time, denoised, linewidth=0.5, color="orange")
    axes[0, 1].set_xlabel("Time [s]", fontsize=11)
    axes[0, 1].set_ylabel("Amplitude", fontsize=11)
    axes[0, 1].set_title(
        f"Wavelet Denoised ({wavelet}, thresh={threshold_used:.1f})",
        fontsize=12,
        fontweight="bold",
    )
    axes[0, 1].grid(True, alpha=0.3)
    if xlim:
        axes[0, 1].set_xlim(xlim)

    # Original spectrogram
    im1 = axes[1, 0].pcolormesh(
        t_orig, f_orig, Sxx_orig_dB, shading="gouraud", cmap="nipy_spectral"
    )
    axes[1, 0].set_xlabel("Time [s]", fontsize=11)
    axes[1, 0].set_ylabel("Frequency [Hz]", fontsize=11)
    axes[1, 0].set_title("Original Spectrogram", fontsize=12, fontweight="bold")
    if fmax:
        axes[1, 0].set_ylim([0, fmax])
    plt.colorbar(im1, ax=axes[1, 0], label="Power/Frequency [dB/Hz]")

    # Denoised spectrogram
    im2 = axes[1, 1].pcolormesh(
        t_clean, f_clean, Sxx_clean_dB, shading="gouraud", cmap="nipy_spectral"
    )
    axes[1, 1].set_xlabel("Time [s]", fontsize=11)
    axes[1, 1].set_ylabel("Frequency [Hz]", fontsize=11)
    axes[1, 1].set_title("Denoised Spectrogram", fontsize=12, fontweight="bold")
    if fmax:
        axes[1, 1].set_ylim([0, fmax])
    plt.colorbar(im2, ax=axes[1, 1], label="Power/Frequency [dB/Hz]")

    fig.suptitle(
        f'Wavelet Denoising Comparison - {time_start.strftime("%Y-%m-%d %H:%M:%S")} UTC',
        fontsize=14,
        fontweight="bold",
        y=0.995,
    )

    plt.tight_layout()
    plt.show()


def plot_wavelet_comparison(
    ears_data, wavelets=["db4", "db8", "db20", "sym8"], xlim=None, figsize=(16, 12)
):
    """
    Compare different wavelet types for denoising.

    Parameters
    ----------
    ears_data : dict
        Dictionary returned by read_ears_file()
    wavelets : list of str, optional
        List of wavelet names to compare
    xlim : tuple, optional
        Time limits (start, end) in seconds for zooming
    figsize : tuple, optional
        Figure size (width, height)

    Examples
    --------
    >>> import dolphain
    >>> data = dolphain.read_ears_file('sample.190')
    >>> dolphain.plot_wavelet_comparison(data)
    >>> dolphain.plot_wavelet_comparison(data, wavelets=['db8', 'sym8'], xlim=(5, 10))
    """
    data = ears_data["data"]
    duration = ears_data["duration"]
    time_start = ears_data["time_start"]

    # Create time array
    time = np.linspace(0, duration, len(data))

    # Create subplots
    n_wavelets = len(wavelets)
    fig, axes = plt.subplots(n_wavelets + 1, 1, figsize=figsize, sharex=True)

    # Plot original
    axes[0].plot(time, data, linewidth=0.5, color="steelblue")
    axes[0].set_ylabel("Amplitude", fontsize=11)
    axes[0].set_title("Original Data", fontsize=12, fontweight="bold")
    axes[0].grid(True, alpha=0.3)

    # Plot each wavelet denoising result
    colors = plt.cm.Set2(np.linspace(0, 1, n_wavelets))
    for i, (wavelet, color) in enumerate(zip(wavelets, colors)):
        denoised, thresh = wavelet_denoise(data, wavelet=wavelet, return_threshold=True)
        axes[i + 1].plot(time, denoised, linewidth=0.5, color=color)
        axes[i + 1].set_ylabel("Amplitude", fontsize=11)
        axes[i + 1].set_title(
            f"Denoised: {wavelet} (thresh={thresh:.1f})", fontsize=12, fontweight="bold"
        )
        axes[i + 1].grid(True, alpha=0.3)

    axes[-1].set_xlabel("Time [s]", fontsize=12)

    if xlim:
        axes[0].set_xlim(xlim)

    fig.suptitle(
        f'Wavelet Comparison - {time_start.strftime("%Y-%m-%d %H:%M:%S")} UTC',
        fontsize=14,
        fontweight="bold",
        y=0.995,
    )

    plt.tight_layout()
    plt.show()
