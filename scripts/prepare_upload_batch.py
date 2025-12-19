import random
from pathlib import Path
import json


def prepare_batch():
    input_file = Path("ears_files_list.txt")
    output_file = Path("upload_batch.json")

    if not input_file.exists():
        print(f"Error: {input_file} not found.")
        return

    print("Reading file list...")
    with open(input_file, "r") as f:
        all_files = [line.strip() for line in f if line.strip()]

    print(f"Total files available: {len(all_files)}")

    # Group by buoy
    buoys = {}
    for file_path in all_files:
        parts = file_path.split("/")
        # Assuming /Volumes/ladcuno8tb0/Deployment/Buoy/Filename
        if len(parts) >= 5:
            deployment = parts[-3]
            buoy = parts[-2]
            key = f"{deployment}/{buoy}"
            if key not in buoys:
                buoys[key] = []
            buoys[key].append(file_path)

    print("\nAvailable datasets:")
    for key, files in buoys.items():
        print(f"  {key}: {len(files)} files")

    # Select batches
    batch = []

    # 1. 2017_South/Buoy150 (Middle chunk)
    key1 = "2017_South/Buoy150"
    if key1 in buoys:
        files = sorted(buoys[key1])
        # Take 200 files from the middle
        start_idx = len(files) // 2
        selection = files[start_idx : start_idx + 200]
        batch.extend(selection)
        print(f"\nSelected {len(selection)} files from {key1}")

    # 2. 2017_West/Buoy140 (Start chunk)
    key2 = "2017_West/Buoy140"
    if key2 in buoys:
        files = sorted(buoys[key2])
        # Take 200 files from the start
        selection = files[0:200]
        batch.extend(selection)
        print(f"Selected {len(selection)} files from {key2}")

    # Save batch
    with open(output_file, "w") as f:
        json.dump(batch, f, indent=2)

    print(f"\nSaved batch of {len(batch)} files to {output_file}")


if __name__ == "__main__":
    prepare_batch()
