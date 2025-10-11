"""
Signal processing functions for acoustic data.

This module provides wavelet-based denoising and other signal processing
capabilities for underwater acoustic recordings.
"""

import numpy as np
import pywt

__all__ = ["threshold", "thresh_wave_coeffs", "wavelet_denoise"]


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
