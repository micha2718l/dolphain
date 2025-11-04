"""
File I/O functions for EARS (Ecological Acoustic Recorder) data files.

This module handles reading binary EARS data files and extracting metadata.
"""

import struct
import datetime
from pathlib import Path
import numpy as np
import tempfile
import shutil
import random

__all__ = ["read_ears_file", "print_file_info", "fetch_huggingface_file", "EARS"]


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


def print_file_info(ears_data, filepath=None):
    """
    Print formatted information about an EARS data file.

    Parameters
    ----------
    ears_data : dict
        Dictionary returned by read_ears_file()
    filepath : str or Path, optional
        Path to the file (for display purposes)

    Examples
    --------
    >>> data = read_ears_file('sample.190')
    >>> print_file_info(data, 'sample.190')
    """
    print("=" * 60)
    print("EARS File Information")
    print("=" * 60)
    if filepath:
        print(f"File: {filepath}")
    print(
        f"Recording start: {ears_data['time_start'].strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )
    print(f"Recording end:   {ears_data['time_end'].strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"Duration: {ears_data['duration']:.2f} seconds")
    print(f"Sampling rate: {ears_data['fs']:,} Hz")
    print(f"Number of samples: {ears_data['n_samples']:,}")
    print(f"Number of timestamp changes: {len(ears_data['timestamps'])}")
    print("=" * 60)


def fetch_huggingface_file(
    dataset_id="ColorSynth/GoMRI-17",
    data_path="2017_South/BUOY200",
    file_extension=".200",
    random_file=True,
    filename=None,
    normalize=True,
    cleanup=True,
):
    """
    Fetch and load an EARS file from HuggingFace Datasets Hub.

    This function seamlessly downloads EARS files from HuggingFace, loads them
    into memory, and optionally cleans up temporary files. Perfect for quick
    exploration and analysis without managing local file storage.

    Parameters
    ----------
    dataset_id : str, optional
        HuggingFace dataset identifier (default: "ColorSynth/GoMRI-17")
    data_path : str, optional
        Path within the dataset to search for files (default: "2017_South/BUOY200")
    file_extension : str, optional
        File extension to filter (default: ".200")
    random_file : bool, optional
        If True, select a random file from available files (default: True)
    filename : str, optional
        Specific filename to download. If provided, ignores random_file parameter
    normalize : bool, optional
        If True, normalize audio data to [-1, 1] range (default: True)
    cleanup : bool, optional
        If True, delete temporary files after loading (default: True)

    Returns
    -------
    dict
        EARS data dictionary from read_ears_file() with additional keys:
        - 'source': 'huggingface'
        - 'dataset_id': the HuggingFace dataset ID
        - 'filename': name of the file
        - 'temp_path': temporary file path (only if cleanup=False)

    Examples
    --------
    >>> # Get a random file (easiest way!)
    >>> data = fetch_huggingface_file()
    >>> print(f"Loaded {data['filename']}, duration: {data['duration']:.2f}s")

    >>> # Get a specific file
    >>> data = fetch_huggingface_file(filename="7178E5DC.200")

    >>> # Get file from different buoy
    >>> data = fetch_huggingface_file(data_path="2017_South/BUOY210")

    >>> # Keep temp file for inspection
    >>> data = fetch_huggingface_file(cleanup=False)
    >>> print(f"Temp file at: {data['temp_path']}")

    Notes
    -----
    Requires `huggingface_hub` package:
        pip install huggingface_hub

    The ColorSynth/GoMRI-17 dataset contains ~1000 EARS recordings from
    autonomous underwater recorders deployed in the Gulf of Mexico. Files
    are ~8.4 MB each and contain ~43 seconds of 192 kHz audio data.
    """
    try:
        from huggingface_hub import HfApi, hf_hub_download
    except ImportError:
        raise ImportError(
            "huggingface_hub is required for this function. "
            "Install it with: pip install huggingface_hub"
        )

    # Initialize HuggingFace API
    api = HfApi()

    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="dolphain_hf_")

    try:
        # Determine which file to download
        if filename is None:
            # List available files
            files = api.list_repo_files(repo_id=dataset_id, repo_type="dataset")

            # Filter for EARS files in the target directory
            ears_files = [
                f
                for f in files
                if f.startswith(data_path) and f.endswith(file_extension)
            ]

            if len(ears_files) == 0:
                raise ValueError(
                    f"No {file_extension} files found in {data_path} "
                    f"of dataset {dataset_id}"
                )

            # Select random or first file
            if random_file:
                selected_file = random.choice(ears_files)
            else:
                selected_file = ears_files[0]
        else:
            # Use specific filename
            selected_file = f"{data_path}/{filename}"

        # Extract just the filename
        file_name = Path(selected_file).name

        # Download file from HuggingFace
        local_path = hf_hub_download(
            repo_id=dataset_id,
            filename=selected_file,
            repo_type="dataset",
            local_dir=temp_dir,
            local_dir_use_symlinks=False,
        )

        # Read the EARS file
        ears_data = read_ears_file(local_path, normalize=normalize)

        # Add metadata about source
        ears_data["source"] = "huggingface"
        ears_data["dataset_id"] = dataset_id
        ears_data["filename"] = file_name
        ears_data["data_path"] = data_path

        # Add temp path if not cleaning up
        if not cleanup:
            ears_data["temp_path"] = local_path

        # Cleanup temporary directory if requested
        if cleanup:
            shutil.rmtree(temp_dir)

        return ears_data

    except Exception as e:
        # Always try to cleanup on error
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
        raise e


class EARS:
    """
    Convenient wrapper class for EARS audio data.

    This class provides an easy-to-use interface for loading, processing,
    and analyzing EARS acoustic data from local files or HuggingFace.

    Parameters
    ----------
    source : str, dict, or None
        Data source. Can be:
        - Path to local EARS file (str)
        - Dictionary from read_ears_file() or fetch_huggingface_file()
        - None to fetch random file from HuggingFace (default)
    normalize : bool, optional
        Normalize audio data to [-1, 1] range (default: True)
    **kwargs : dict
        Additional arguments passed to fetch_huggingface_file() if source is None

    Attributes
    ----------
    data : ndarray
        Audio sample data
    fs : int
        Sampling rate (Hz)
    duration : float
        Recording duration (seconds)
    time_start : datetime
        Recording start time
    time_end : datetime
        Recording end time
    filename : str
        Source filename (if available)
    metadata : dict
        Full metadata dictionary

    Examples
    --------
    >>> # Easiest way - random file from HuggingFace
    >>> ears = EARS()
    >>> print(f"Loaded {ears.filename}: {ears.duration:.2f}s")

    >>> # From local file
    >>> ears = EARS('data/sample.200')

    >>> # From specific HuggingFace file
    >>> ears = EARS(filename='7178E5DC.200')

    >>> # Access data
    >>> print(ears.data.shape)
    >>> print(f"Sampling rate: {ears.fs} Hz")

    >>> # Use with existing data dict
    >>> data = fetch_huggingface_file()
    >>> ears = EARS(data)
    """

    def __init__(self, source=None, normalize=True, **kwargs):
        """Initialize EARS object from various sources."""
        if source is None:
            # Fetch from HuggingFace with default settings
            self.metadata = fetch_huggingface_file(normalize=normalize, **kwargs)
        elif isinstance(source, dict):
            # Already loaded data
            self.metadata = source
        elif isinstance(source, (str, Path)):
            # Local file path
            self.metadata = read_ears_file(source, normalize=normalize)
            self.metadata["filename"] = Path(source).name
            self.metadata["source"] = "local"
        else:
            raise TypeError(
                f"source must be None, str, Path, or dict, got {type(source)}"
            )

        # Create convenient attributes
        self.data = self.metadata["data"]
        self.fs = self.metadata["fs"]
        self.duration = self.metadata["duration"]
        self.time_start = self.metadata["time_start"]
        self.time_end = self.metadata["time_end"]
        self.filename = self.metadata.get("filename", "unknown")

    def __repr__(self):
        """String representation of EARS object."""
        source = self.metadata.get("source", "unknown")
        return (
            f"EARS(filename='{self.filename}', "
            f"duration={self.duration:.2f}s, "
            f"fs={self.fs}Hz, "
            f"source='{source}')"
        )

    def info(self):
        """Print detailed information about the recording."""
        print_file_info(self.metadata, self.filename)

    def denoise(self, wavelet="db20", **kwargs):
        """
        Apply wavelet denoising to the audio data.

        Parameters
        ----------
        wavelet : str, optional
            Wavelet name (default: 'db20')
        **kwargs : dict
            Additional arguments passed to wavelet_denoise()

        Returns
        -------
        ndarray
            Denoised audio data
        """
        from .signal import wavelet_denoise

        return wavelet_denoise(self.data, wavelet=wavelet, **kwargs)

    def plot(self, plot_type="overview", **kwargs):
        """
        Plot the audio data.

        Parameters
        ----------
        plot_type : str, optional
            Type of plot: 'waveform', 'spectrogram', 'overview', 
            'denoising' (default: 'overview')
        **kwargs : dict
            Additional arguments passed to plotting functions

        Examples
        --------
        >>> ears = EARS()
        >>> ears.plot()  # Overview plot
        >>> ears.plot('spectrogram', fmax=20000)
        >>> ears.plot('denoising', wavelet='db8')
        """
        from . import plotting

        plot_funcs = {
            "waveform": plotting.plot_waveform,
            "spectrogram": plotting.plot_spectrogram,
            "overview": plotting.plot_overview,
            "denoising": plotting.plot_denoising_comparison,
        }

        if plot_type not in plot_funcs:
            raise ValueError(
                f"plot_type must be one of {list(plot_funcs.keys())}, got '{plot_type}'"
            )

        plot_funcs[plot_type](self.metadata, **kwargs)

    def detect_whistles(self, **kwargs):
        """
        Detect dolphin whistles in the recording.

        Parameters
        ----------
        **kwargs : dict
            Arguments passed to detect_whistles()

        Returns
        -------
        list of dict
            Detected whistles with time, frequency, and power information
        """
        from .signal import detect_whistles

        return detect_whistles(self.data, self.fs, **kwargs)
