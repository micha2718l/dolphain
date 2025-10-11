"""
Signal processing functions for acoustic data.

This module provides wavelet-based denoising and other signal processing
capabilities for underwater acoustic recordings.
"""

import numpy as np
import pywt
from scipy import signal as sp_signal
from scipy.ndimage import maximum_filter

__all__ = ["threshold", "thresh_wave_coeffs", "wavelet_denoise", "detect_whistles"]


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

    Notes
    -----
    - Soft thresholding: shrinks coefficients towards zero by delta
    - Hard thresholding: keeps coefficients above threshold, zeros others
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
        Common options: 'db4', 'db8', 'db20', 'sym4', 'sym8', 'coif5'
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
    >>> import dolphain
    >>> # Read data
    >>> data = dolphain.read_ears_file('sample.190')
    >>> # Denoise
    >>> denoised = dolphain.wavelet_denoise(data['data'])
    >>> denoised, thresh = dolphain.wavelet_denoise(data['data'], return_threshold=True)
    >>> denoised = dolphain.wavelet_denoise(data['data'], wavelet='db8', hard_threshold=True)

    Notes
    -----
    The function uses the VisuShrink method (Donoho & Johnstone, 1994):
    - Sigma is estimated as MAD / 0.6745, where MAD is the median absolute
      deviation of the finest-scale wavelet coefficients
    - Universal threshold = sigma * sqrt(2 * log(N))
    - Soft thresholding produces smoother results
    - Hard thresholding preserves more sharp features

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


def detect_whistles(
    data,
    fs,
    freq_range=(2000, 20000),
    min_duration=0.1,
    nperseg=2048,
    noverlap=None,
    power_threshold_percentile=85,
    min_contour_points=5,
):
    """
    Detect dolphin whistles in acoustic data.

    Whistles are narrow-band frequency-modulated signals typically in the
    2-20 kHz range. This function uses spectrogram-based ridge detection
    to identify and extract whistle contours.

    Parameters
    ----------
    data : array_like
        Input acoustic data
    fs : int
        Sampling frequency in Hz
    freq_range : tuple of float, optional
        (min_freq, max_freq) in Hz for whistle detection (default: 2000-20000 Hz)
    min_duration : float, optional
        Minimum whistle duration in seconds (default: 0.1)
    nperseg : int, optional
        Length of each FFT segment for spectrogram (default: 2048)
    noverlap : int, optional
        Number of samples to overlap between segments. If None, uses 75% overlap
    power_threshold_percentile : float, optional
        Percentile threshold for detecting ridges in spectrogram (default: 85)
    min_contour_points : int, optional
        Minimum number of time points for a valid contour (default: 5)

    Returns
    -------
    whistles : list of dict
        List of detected whistles, where each whistle is a dictionary with:
        - 'time': array of time points (seconds)
        - 'frequency': array of frequency values (Hz)
        - 'power': array of power values (dB)
        - 'start_time': whistle start time (seconds)
        - 'end_time': whistle end time (seconds)
        - 'duration': whistle duration (seconds)
        - 'min_freq': minimum frequency (Hz)
        - 'max_freq': maximum frequency (Hz)
        - 'mean_freq': mean frequency (Hz)

    Examples
    --------
    >>> import dolphain
    >>> # Read data
    >>> data = dolphain.read_ears_file('sample.210')
    >>> # Detect whistles
    >>> whistles = dolphain.detect_whistles(data['data'], data['fs'])
    >>> print(f"Found {len(whistles)} whistles")
    >>> # Get first whistle details
    >>> if whistles:
    ...     w = whistles[0]
    ...     print(f"Duration: {w['duration']:.2f}s, Freq range: {w['min_freq']:.0f}-{w['max_freq']:.0f} Hz")

    Notes
    -----
    The detection algorithm:
    1. Band-pass filters data to whistle frequency range (2-20 kHz typical)
    2. Computes high-resolution spectrogram
    3. Identifies ridges (local frequency maxima) in the spectrogram
    4. Extracts contours by tracking ridges across time
    5. Filters by minimum duration and contour quality

    Whistles are characterized by:
    - Narrow-band frequency modulation
    - Typical duration: 0.5-1.5 seconds
    - Frequency range: 2-20 kHz for most dolphin species
    - Signature whistles are unique identifiers for individuals

    References
    ----------
    Janik, V. M., & Sayigh, L. S. (2013). Communication in bottlenose dolphins:
    50 years of signature whistle research. Journal of Comparative Physiology A,
    199(6), 479-489.
    """
    data = np.asarray(data)

    # Set default overlap to 75%
    if noverlap is None:
        noverlap = int(0.75 * nperseg)

    # Band-pass filter to whistle frequency range
    nyquist = fs / 2.0
    low = max(freq_range[0] / nyquist, 0.001)  # Avoid zero
    high = min(freq_range[1] / nyquist, 0.999)  # Avoid Nyquist

    # Design Butterworth band-pass filter
    sos = sp_signal.butter(4, [low, high], btype="bandpass", output="sos")
    filtered_data = sp_signal.sosfiltfilt(sos, data)

    # Compute high-resolution spectrogram
    f, t, Sxx = sp_signal.spectrogram(
        filtered_data,
        fs=fs,
        nperseg=nperseg,
        noverlap=noverlap,
        window="hann",
        scaling="density",
    )

    # Convert to dB
    Sxx_dB = 10 * np.log10(Sxx + 1e-12)

    # Find frequency indices within our range
    freq_mask = (f >= freq_range[0]) & (f <= freq_range[1])
    f_filtered = f[freq_mask]
    Sxx_filtered = Sxx_dB[freq_mask, :]

    if Sxx_filtered.size == 0:
        return []

    # Threshold based on power percentile
    power_threshold = np.percentile(Sxx_filtered, power_threshold_percentile)

    # Find ridges: local maxima in frequency direction at each time step
    # Use maximum_filter to find local maxima
    neighborhood_size = 3  # Look at neighboring frequencies
    local_max = (
        maximum_filter(Sxx_filtered, size=(neighborhood_size, 1)) == Sxx_filtered
    )

    # Apply power threshold
    strong_points = Sxx_filtered > power_threshold
    ridge_mask = local_max & strong_points

    # Extract contours by connecting ridges across time
    whistles = []

    # For each time point, find the strongest ridge
    for time_idx in range(ridge_mask.shape[1]):
        freq_indices = np.where(ridge_mask[:, time_idx])[0]

        if len(freq_indices) > 0:
            # Get the strongest frequency component at this time
            powers = Sxx_filtered[freq_indices, time_idx]
            strongest_idx = freq_indices[np.argmax(powers)]

            # Try to add to existing contour or start new one
            added = False
            for whistle in whistles:
                if len(whistle["freq_indices"]) > 0:
                    last_freq_idx = whistle["freq_indices"][-1]
                    last_time_idx = whistle["time_indices"][-1]

                    # Check if this point continues the contour
                    # Allow frequency jumps within reasonable range and only consecutive time steps
                    freq_diff = abs(strongest_idx - last_freq_idx)
                    time_diff = time_idx - last_time_idx

                    if (
                        time_diff == 1 and freq_diff < 10
                    ):  # Adjacent in time, close in frequency
                        whistle["time_indices"].append(time_idx)
                        whistle["freq_indices"].append(strongest_idx)
                        added = True
                        break

            if not added:
                # Start new contour
                whistles.append(
                    {"time_indices": [time_idx], "freq_indices": [strongest_idx]}
                )

    # Convert contours to whistle dictionaries and filter
    filtered_whistles = []

    for contour in whistles:
        if len(contour["time_indices"]) < min_contour_points:
            continue

        time_indices = np.array(contour["time_indices"])
        freq_indices = np.array(contour["freq_indices"])

        # Get actual time and frequency values
        times = t[time_indices]
        freqs = f_filtered[freq_indices]
        powers = Sxx_filtered[freq_indices, time_indices]

        # Calculate duration
        duration = times[-1] - times[0]

        # Filter by minimum duration
        if duration < min_duration:
            continue

        # Create whistle dictionary
        whistle = {
            "time": times,
            "frequency": freqs,
            "power": powers,
            "start_time": times[0],
            "end_time": times[-1],
            "duration": duration,
            "min_freq": freqs.min(),
            "max_freq": freqs.max(),
            "mean_freq": freqs.mean(),
        }

        filtered_whistles.append(whistle)

    return filtered_whistles
