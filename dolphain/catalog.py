import pandas as pd
from huggingface_hub import HfFileSystem
import struct
import datetime
from pathlib import Path
import os
import io

try:
    from importlib.resources import files
except ImportError:
    # Fallback for Python < 3.9
    from importlib_resources import files

# Constants
RECORD_SIZE = 512
SAMPLES_PER_RECORD = 250
FS = 192000
FS_TIME = 32000


def parse_header_timestamp(header, filename):
    """
    Parse the timestamp from the 12-byte header of an EARS file.
    """
    if filename.startswith("7"):
        epoch = datetime.datetime(2015, 10, 27)
    else:
        epoch = datetime.datetime(2000, 1, 1)

    try:
        # The timestamp is in bytes 6-11 (0-indexed)
        # struct.unpack("6x6B", header) skips 6 bytes, then reads 6 unsigned bytes
        s = struct.unpack("6x6B", header[:12])
        timestamp_seconds = (
            ((s[0] - 14) / 16) * 2**40
            + s[1] * 2**32
            + s[2] * 2**24
            + s[3] * 2**16
            + s[4] * 2**8
            + s[5]
        ) / FS_TIME
        return epoch + datetime.timedelta(seconds=timestamp_seconds)
    except Exception as e:
        # print(f"Error parsing header for {filename}: {e}")
        return None


def get_file_info(fs, file_path):
    """
    Get start and end time for a file.
    """
    try:
        info = fs.info(file_path)
        size = info["size"]
        filename = file_path.split("/")[-1]

        # Read first 12 bytes for header
        with fs.open(file_path, "rb") as f:
            header = f.read(12)

        start_time = parse_header_timestamp(header, filename)
        if start_time is None:
            return None

        n_records = size // RECORD_SIZE
        n_samples = n_records * SAMPLES_PER_RECORD
        duration = n_samples / FS
        end_time = start_time + datetime.timedelta(seconds=duration)

        return {
            "file_path": file_path,
            "filename": filename,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "size": size,
            "n_samples": n_samples,
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def build_catalog(
    dataset_id="ColorSynth/GoMRI-17", output_file="catalog.csv", path_pattern=None
):
    fs = HfFileSystem()
    print(f"Scanning {dataset_id}...")

    # Find all files recursively
    # We know the structure is datasets/ColorSynth/GoMRI-17/...
    # We can try to be smart or just glob everything
    print("Globbing all files (this may take a moment)...")

    if path_pattern:
        glob_pattern = path_pattern
    else:
        glob_pattern = f"datasets/{dataset_id}/**"

    # Using ** to find all files
    all_files = fs.glob(glob_pattern)

    extensions = [".130", ".190", ".210", ".200", ".dat"]
    files = [f for f in all_files if any(f.endswith(ext) for ext in extensions)]

    print(f"Found {len(files)} relevant files. Processing headers...")

    records = []
    for i, file_path in enumerate(files):
        if i % 10 == 0:
            print(f"Processed {i}/{len(files)}")

        info = get_file_info(fs, file_path)
        if info:
            records.append(info)

    df = pd.DataFrame(records)
    if not df.empty:
        df = df.sort_values("start_time")
        df.to_csv(output_file, index=False)
        print(f"Catalog saved to {output_file} with {len(df)} records.")
    else:
        print("No valid records found.")
    return df


class Catalog:
    def __init__(self, catalog_path=None):
        """
        Initialize a Catalog from a CSV file.

        Parameters
        ----------
        catalog_path : str, optional
            Path to a catalog CSV file. If None, uses the built-in default catalog
            which contains 1000 sample files from the EARS dataset.
        """
        if catalog_path is None:
            # Use the built-in default catalog
            try:
                # Use modern importlib.resources (Python 3.9+)
                catalog_path = str(
                    files("dolphain").joinpath("data/default_catalog.csv")
                )
            except Exception:
                # Fallback for development installations
                module_dir = Path(__file__).parent
                catalog_path = module_dir / "data" / "default_catalog.csv"
                catalog_path = str(catalog_path)

        if os.path.exists(catalog_path):
            self.df = pd.read_csv(catalog_path)
            self.df["start_time"] = pd.to_datetime(self.df["start_time"])
            self.df["end_time"] = pd.to_datetime(self.df["end_time"])
        else:
            self.df = pd.DataFrame()

    def query(self, start_time, end_time):
        """
        Find files that overlap with the requested time range.
        """
        if self.df.empty:
            return pd.DataFrame()

        # Files that start before the requested end AND end after the requested start
        mask = (self.df["start_time"] < end_time) & (self.df["end_time"] > start_time)
        return self.df[mask].sort_values("start_time")


if __name__ == "__main__":
    build_catalog()
