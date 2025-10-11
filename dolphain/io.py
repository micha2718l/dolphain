"""
File I/O functions for EARS (Ecological Acoustic Recorder) data files.

This module handles reading binary EARS data files and extracting metadata.
"""

import struct
import datetime
from pathlib import Path
import numpy as np

__all__ = ["read_ears_file", "print_file_info"]


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
