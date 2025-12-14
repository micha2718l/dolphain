import dolphain
from dolphain.io import fetch_huggingface_file, read_ears_file
import datetime
from pathlib import Path


def check_filename_timestamp():
    # Fetch a random file
    print("Fetching a file from HuggingFace...")
    data = fetch_huggingface_file(cleanup=False)
    filepath = data["temp_path"]
    filename = data["filename"]

    print(f"File: {filename}")
    print(f"Start Time (from content): {data['time_start']}")

    # Parse filename
    hex_str = Path(filename).stem
    try:
        val = int(hex_str, 16)
        print(f"Filename hex value: {val}")

        if filename.startswith("7"):
            epoch = datetime.datetime(2015, 10, 27)
        else:
            epoch = datetime.datetime(2000, 1, 1)

        calculated_time = epoch + datetime.timedelta(seconds=val / 32000)
        print(f"Calculated Time (from filename): {calculated_time}")

        diff = abs((data["time_start"] - calculated_time).total_seconds())
        print(f"Difference: {diff} seconds")

    except ValueError:
        print("Filename is not valid hex")


if __name__ == "__main__":
    check_filename_timestamp()
