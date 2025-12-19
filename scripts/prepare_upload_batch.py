import random
from pathlib import Path
import json
import argparse
import csv


def load_catalog_files():
    """Load set of files already in the catalog to avoid re-uploading."""
    catalog_path = Path("dolphain/data/default_catalog.csv")
    if not catalog_path.exists():
        return set()

    existing = set()
    with open(catalog_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Catalog stores relative paths or keys?
            # Usually catalog has 'deployment', 'buoy', 'filename'
            # We construct the key to match what we might find
            pass
            # Actually, let's just rely on the upload script to skip existing.
            # But for random selection, it's better to filter first so we don't pick 200 already uploaded files.
    return existing


def prepare_batch():
    parser = argparse.ArgumentParser(description="Prepare a batch of files for upload.")
    parser.add_argument("--random", action="store_true", help="Select random files.")
    parser.add_argument(
        "--contiguous", action="store_true", help="Select a contiguous block of files."
    )
    parser.add_argument(
        "--count", type=int, default=200, help="Number of files to select."
    )
    parser.add_argument("--buoy", type=str, help="Filter by buoy (e.g., Buoy150).")
    args = parser.parse_args()

    input_file = Path("ears_files_list.txt")
    output_file = Path("upload_batch.json")
    catalog_path = Path("dolphain/data/default_catalog.csv")

    if not input_file.exists():
        print(f"Error: {input_file} not found. Run parse_drive_listing.py first.")
        return

    # Load existing catalog to exclude files (unless contiguous)
    existing_filenames = set()
    if catalog_path.exists():
        with open(catalog_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "filename" in row:
                    existing_filenames.add(row["filename"])

    print(f"Loaded {len(existing_filenames)} existing files from catalog.")

    print("Reading file list...")
    with open(input_file, "r") as f:
        all_files = [line.strip() for line in f if line.strip()]

    print(f"Total files available on drive: {len(all_files)}")

    # Filter out files already in catalog IF NOT contiguous
    # If contiguous, we want the whole block even if some are uploaded
    candidates = []
    if args.contiguous:
        candidates = all_files
    else:
        for fpath in all_files:
            fname = Path(fpath).name
            if fname not in existing_filenames:
                candidates.append(fpath)

    print(f"Files available for selection: {len(candidates)}")

    if not candidates:
        print("No files available!")
        return

    batch = []

    if args.contiguous:
        # Contiguous selection
        # 1. Group by buoy
        buoys = {}
        for file_path in candidates:
            parts = file_path.split("/")
            if len(parts) >= 5:
                deployment = parts[-3]
                buoy = parts[-2]
                key = f"{deployment}/{buoy}"
                if key not in buoys:
                    buoys[key] = []
                buoys[key].append(file_path)

        # 2. Pick random buoy
        if args.buoy:
            # Filter keys
            keys = [k for k in buoys.keys() if args.buoy in k]
            if not keys:
                print(f"No files found for buoy {args.buoy}")
                return
            selected_key = keys[0]  # Just take the first match
        else:
            selected_key = random.choice(list(buoys.keys()))

        print(f"Selected dataset: {selected_key}")

        # 3. Sort files (assuming filename contains timestamp or is sortable)
        files = sorted(buoys[selected_key])
        total_files = len(files)

        # 4. Pick random start
        if total_files <= args.count:
            batch = files
            print(f"Taking all {len(batch)} files from {selected_key}")
        else:
            max_start = total_files - args.count
            start_idx = random.randint(0, max_start)
            batch = files[start_idx : start_idx + args.count]
            print(
                f"Selected {len(batch)} files starting at index {start_idx} from {selected_key}"
            )

    elif args.random:
        # Random selection
        count = min(args.count, len(candidates))
        batch = random.sample(candidates, count)
        print(f"\nSelected {len(batch)} random files.")

    elif args.buoy:
        # Filter by buoy
        buoy_candidates = [f for f in candidates if args.buoy in f]
        count = min(args.count, len(buoy_candidates))
        batch = buoy_candidates[
            :count
        ]  # Take first N, or maybe random? Let's take first N for deterministic behavior unless random specified
        print(f"\nSelected {len(batch)} files for {args.buoy}.")

    else:
        # Default behavior (original hardcoded logic, but using candidates)
        # We'll just default to random if nothing specified, or maybe the first N
        print("No specific selection criteria. Selecting first N files.")
        count = min(args.count, len(candidates))
        batch = candidates[:count]

    # Save batch
    with open(output_file, "w") as f:
        json.dump(batch, f, indent=2)

    print(f"\nSaved batch of {len(batch)} files to {output_file}")


if __name__ == "__main__":
    prepare_batch()
