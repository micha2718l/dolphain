"""
EARS (Ecological Acoustic Recorder) Data Reader and Visualization

This module provides functions to read and visualize EARS binary data files
from underwater acoustic recordings in the Gulf of Mexico.

Author: Generated from dolphain.ipynb
Date: 2025-10-08
"""

import struct
import datetime
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pywt  # PyWavelets for wavelet denoising


def read_ears_file(filepath, normalize=False):
    """
    Read an EARS binary data file.

    Parameters
    ----------
    filepath : str or Path
        Path to the EARS data file (.130, .190, etc.)
    normalize : bool, optional
        If True, normalize data to [-1, 1] range

    Returns
    -------
    dict
        Dictionary containing:
        - 'data': numpy array of acoustic samples
        - 'fs': sampling rate (Hz)
        - 'time_start': datetime of recording start
        - 'time_end': datetime of recording end
        - 'timestamps': list of timestamps from headers
        - 'duration': duration in seconds
        - 'n_samples': number of samples

    Examples
    --------
    >>> ears_data = read_ears_file('sample_data/71621DC7.190')
    >>> print(f"Duration: {ears_data['duration']:.2f} seconds")
    >>> print(f"Sampling rate: {ears_data['fs']} Hz")
    """
    # Constants
    RECORD_SIZE = 512
    HEADER_SIZE = 12
    SAMPLES_PER_RECORD = 250
    FS = 192000  # Sampling rate in Hz
    FS_TIME = 32000  # Timestamp sampling rate

    # Determine epoch based on filename
    filename = Path(filepath).name
    if filename[0] == "7":
        epoch = datetime.datetime(2015, 10, 27)
    else:
        epoch = datetime.datetime(2000, 1, 1)

    # Read binary file
    with open(filepath, "rb") as f:
        raw_data = f.read()

    # Parse records
    data = []
    headers = []
    timestamps = []
    n_records = len(raw_data) // RECORD_SIZE

    for i in range(n_records):
        offset = RECORD_SIZE * i

        # Extract header
        header = raw_data[offset : offset + HEADER_SIZE]

        # Extract data (250 16-bit signed integers, big-endian)
        samples = struct.unpack_from(">250h", raw_data, offset=offset + HEADER_SIZE)
        data.extend(samples)

        # Parse timestamp from header (only when it changes)
        if i == 0 or header != headers[-1]:
            headers.append(header)
            # Unpack timestamp bytes (6 bytes starting at byte 6)
            s = struct.unpack("6x6B", header)
            timestamp_seconds = (
                ((s[0] - 14) / 16) * 2**40
                + s[1] * 2**32
                + s[2] * 2**24
                + s[3] * 2**16
                + s[4] * 2**8
                + s[5]
            ) / FS_TIME
            timestamp = epoch + datetime.timedelta(seconds=timestamp_seconds)
            timestamps.append(timestamp)

    # Convert to numpy array
    data = np.array(data, dtype=np.float64)

    # Normalize if requested
    if normalize:
        data -= np.mean(data)
        data /= np.max(np.abs(data))

    # Calculate timing information
    time_start = timestamps[0]
    duration = len(data) / FS
    time_end = time_start + datetime.timedelta(seconds=duration)

    return {
        "data": data,
        "fs": FS,
        "time_start": time_start,
        "time_end": time_end,
        "timestamps": timestamps,
        "duration": duration,
        "n_samples": len(data),
    }


# =============================================================================
# Wavelet Denoising Functions
# =============================================================================


def threshold(x_in, delta, hard=False):
    """
    Apply soft or hard thresholding to data.

    Parameters
    ----------
    x_in : array_like
        Input data to threshold
    delta : float
        Threshold value
    hard : bool, optional
        If True, use hard thresholding; if False, use soft thresholding

    Returns
    -------
    ndarray
        Thresholded data
    """
    x_in = np.asarray(x_in).copy()
    x_thresh_indices = np.abs(x_in) < delta

    if not hard:
        # Soft thresholding: shrink values toward zero
        x_in = np.sign(x_in) * (np.abs(x_in) - delta)

    # Set values below threshold to zero
    x_in[x_thresh_indices] = 0
    return x_in


def thresh_wave_coeffs(wavelet_coeffs, delta, hard=False):
    """
    Apply thresholding to wavelet coefficients.

    Parameters
    ----------
    wavelet_coeffs : list of arrays
        Wavelet decomposition coefficients from pywt.wavedec
    delta : float
        Threshold value
    hard : bool, optional
        If True, use hard thresholding; if False, use soft thresholding

    Returns
    -------
    list of arrays
        Thresholded wavelet coefficients
    """
    return [
        np.asarray(threshold(coeff, delta=delta, hard=hard)) for coeff in wavelet_coeffs
    ]


def wavelet_denoise(
    data, wavelet="db20", thresh=None, return_threshold=False, hard_threshold=False
):
    """
    Denoise acoustic data using wavelet thresholding.

    This function uses the Universal Threshold (VisuShrink) method:
    threshold = sigma * sqrt(2 * log(N))
    where sigma is estimated from the median absolute deviation of the
    finest-scale wavelet coefficients.

    Parameters
    ----------
    data : array_like
        Input acoustic data to denoise
    wavelet : str, optional
        Wavelet name (default: 'db20', Daubechies 20)
        Common options: 'db4', 'db8', 'db20', 'sym4', 'coif5'
    thresh : float, optional
        Threshold value. If None, calculated using universal threshold
    return_threshold : bool, optional
        If True, return both denoised data and threshold value
    hard_threshold : bool, optional
        If True, use hard thresholding; if False, use soft thresholding

    Returns
    -------
    denoised_data : ndarray
        Denoised acoustic data
    threshold_value : float (only if return_threshold=True)
        The threshold value used

    Examples
    --------
    >>> data = ears_data['data']
    >>> denoised = wavelet_denoise(data)
    >>> denoised, thresh = wavelet_denoise(data, return_threshold=True)
    >>> denoised = wavelet_denoise(data, wavelet='db8', hard_threshold=True)

    Notes
    -----
    The function uses the VisuShrink method (Donoho & Johnstone, 1994):
    - Sigma is estimated as MAD / 0.6745, where MAD is the median absolute
      deviation of the finest-scale wavelet coefficients
    - Universal threshold = sigma * sqrt(2 * log(N))

    References
    ----------
    Donoho, D. L., & Johnstone, I. M. (1994). Ideal spatial adaptation by
    wavelet shrinkage. Biometrika, 81(3), 425-455.
    """
    # Convert to numpy array and remove mean
    data = np.asarray(data)
    data = data - data.mean()

    # Perform wavelet decomposition
    wavelet_coeffs = pywt.wavedec(data, wavelet)

    # Calculate threshold if not provided
    if thresh is None:
        # Get finest-scale detail coefficients
        detail_coeffs = wavelet_coeffs[-1]

        # Estimate noise standard deviation using MAD
        # 0.6745 is the MAD for standard normal distribution
        denom = 0.6744897501960817
        sigma = np.median(np.abs(detail_coeffs)) / denom

        # Universal threshold (VisuShrink)
        thresh = sigma * np.sqrt(2 * np.log(len(data)))

    # Apply threshold to coefficients
    wavelet_coeffs_thresholded = thresh_wave_coeffs(
        wavelet_coeffs, delta=thresh, hard=hard_threshold
    )

    # Reconstruct signal
    denoised = pywt.waverec(wavelet_coeffs_thresholded, wavelet)

    # Ensure same length (wavelet transform may add samples)
    if len(denoised) > len(data):
        denoised = denoised[: len(data)]

    if return_threshold:
        return denoised, thresh
    return denoised


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
    >>> ears_data = read_ears_file('sample_data/71621DC7.190')
    >>> plot_waveform(ears_data)
    >>> plot_waveform(ears_data, xlim=(5, 10))  # Zoom to 5-10 seconds
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
    >>> ears_data = read_ears_file('sample_data/71621DC7.190')
    >>> plot_spectrogram(ears_data, fmax=5000)  # Show up to 5 kHz
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
    >>> ears_data = read_ears_file('sample_data/71621DC7.190')
    >>> plot_overview(ears_data, fmax=5000, xlim_zoom=(5, 10))
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


def print_file_info(ears_data, filepath=None):
    """
    Print a formatted summary of EARS file information.

    Parameters
    ----------
    ears_data : dict
        Dictionary returned by read_ears_file()
    filepath : str or Path, optional
        Path to the file (for display purposes)

    Examples
    --------
    >>> ears_data = read_ears_file('sample_data/71621DC7.190')
    >>> print_file_info(ears_data, 'sample_data/71621DC7.190')
    """
    if filepath:
        print(f"File: {filepath}")
    print(f"Recording start: {ears_data['time_start']}")
    print(f"Recording end: {ears_data['time_end']}")
    print(f"Duration: {ears_data['duration']:.2f} seconds")
    print(f"Number of samples: {ears_data['n_samples']:,}")
    print(f"Sampling rate: {ears_data['fs']:,} Hz")


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
    >>> data = read_ears_file('sample.190')
    >>> plot_denoising_comparison(data)
    >>> plot_denoising_comparison(data, wavelet='db8', xlim=(5, 15), fmax=5000)
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
    >>> data = read_ears_file('sample.190')
    >>> plot_wavelet_comparison(data)
    >>> plot_wavelet_comparison(data, wavelets=['db8', 'sym8'], xlim=(5, 10))
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
