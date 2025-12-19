import json
import csv
import struct
import datetime
import os
from pathlib import Path
from huggingface_hub import HfApi, CommitOperationAdd

# Constants
RECORD_SIZE = 512
HEADER_SIZE = 12
SAMPLES_PER_RECORD = 250
FS = 192000
FS_TIME = 32000
DATASET_ID = "ColorSynth/GoMRI-17"
CATALOG_PATH = Path("dolphain/data/default_catalog.csv")
PROGRESS_FILE = Path("upload_progress.json")
BATCH_SIZE = 50  # Number of files per commit


def get_ears_metadata(filepath):
    """Extract metadata from EARS file header without reading whole file."""
    filename = Path(filepath).name
    file_size = os.path.getsize(filepath)

    # Determine epoch
    if filename[0] == "7":
        epoch = datetime.datetime(2015, 10, 27)
    else:
        epoch = datetime.datetime(2000, 1, 1)

    with open(filepath, "rb") as f:
        header = f.read(HEADER_SIZE)

    if len(header) < HEADER_SIZE:
        raise ValueError(f"File too small: {filepath}")

    # Parse timestamp
    s = struct.unpack("6x6B", header)
    timestamp_seconds = (
        ((s[0] - 14) / 16) * 2**40
        + s[1] * 2**32
        + s[2] * 2**24
        + s[3] * 2**16
        + s[4] * 2**8
        + s[5]
    ) / FS_TIME

    start_time = epoch + datetime.timedelta(seconds=timestamp_seconds)

    # Calculate duration and samples
    n_records = file_size // RECORD_SIZE
    n_samples = n_records * SAMPLES_PER_RECORD
    duration = n_samples / FS
    end_time = start_time + datetime.timedelta(seconds=duration)

    return {
        "filename": filename,
        "start_time": start_time,
        "end_time": end_time,
        "duration": duration,
        "size": file_size,
        "n_samples": n_samples,
    }


def load_progress():
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_progress(uploaded_files):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(list(uploaded_files), f)


def process_batch(
    api, operations, metadata_list, file_paths, uploaded_files, writer, csvfile
):
    """Execute a batch upload and update catalog/progress."""
    if not operations:
        return

    print(f"  Uploading batch of {len(operations)} files...")
    try:
        api.create_commit(
            repo_id=DATASET_ID,
            repo_type="dataset",
            operations=operations,
            commit_message=f"Add batch of {len(operations)} EARS files",
        )
        print("  ✓ Commit successful")

        # Update catalog
        for meta in metadata_list:
            writer.writerow(meta)
        csvfile.flush()

        # Update progress
        for fp in file_paths:
            uploaded_files.add(fp)
        save_progress(uploaded_files)
        print("  ✓ Catalog and progress updated")

    except Exception as e:
        print(f"  ✗ Error uploading batch: {e}")
        # We don't update progress or catalog if commit fails
        # This ensures we can retry later


def main():
    # Check authentication first
    try:
        user = HfApi().whoami()
        print(f"Authenticated as: {user['name']}")
    except Exception:
        print("Error: Not authenticated with HuggingFace.")
        print("Please run: .venv/bin/hf auth login")
        return

    # Load batch
    with open("upload_batch.json", "r") as f:
        batch_files = json.load(f)

    print(f"Loaded batch of {len(batch_files)} files")

    # Load progress
    uploaded_files = load_progress()
    print(f"Already uploaded: {len(uploaded_files)}")

    # Initialize HF API
    api = HfApi()

    # Load existing catalog to avoid duplicates
    existing_catalog_files = set()
    if CATALOG_PATH.exists():
        with open(CATALOG_PATH, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_catalog_files.add(row["filename"])
    print(f"Existing catalog entries: {len(existing_catalog_files)}")

    # Open catalog for appending
    # Check if we need to write header
    write_header = not CATALOG_PATH.exists()

    with open(CATALOG_PATH, "a", newline="") as csvfile:
        fieldnames = [
            "file_path",
            "filename",
            "start_time",
            "end_time",
            "duration",
            "size",
            "n_samples",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        # Batch containers
        current_ops = []
        current_meta = []
        current_paths = []

        for file_path_str in batch_files:
            if file_path_str in uploaded_files:
                continue

            file_path = Path(file_path_str)
            if not file_path.exists():
                print(f"Warning: File not found {file_path}")
                continue

            # Check if already in catalog (by filename)
            if file_path.name in existing_catalog_files:
                print(f"Skipping {file_path.name} (already in catalog)")
                uploaded_files.add(file_path_str)
                save_progress(uploaded_files)
                continue

            try:
                # 1. Get Metadata
                meta = get_ears_metadata(file_path)

                # 2. Determine HF path
                parts = file_path.parts
                try:
                    if "2017_South" in parts:
                        idx = parts.index("2017_South")
                    elif "2017_West" in parts:
                        idx = parts.index("2017_West")
                    else:
                        idx = len(parts) - 3
                    hf_path_in_repo = "/".join(parts[idx:])
                except ValueError:
                    hf_path_in_repo = file_path.name

                # 3. Add to batch
                print(f"Queuing {file_path.name}...")

                # Create operation
                op = CommitOperationAdd(
                    path_in_repo=hf_path_in_repo, path_or_fileobj=file_path
                )
                current_ops.append(op)

                # Create catalog entry
                catalog_entry = {
                    "file_path": f"datasets/{DATASET_ID}/{hf_path_in_repo}",
                    "filename": meta["filename"],
                    "start_time": meta["start_time"],
                    "end_time": meta["end_time"],
                    "duration": meta["duration"],
                    "size": meta["size"],
                    "n_samples": meta["n_samples"],
                }
                current_meta.append(catalog_entry)
                current_paths.append(file_path_str)

                # 4. Process batch if full
                if len(current_ops) >= BATCH_SIZE:
                    process_batch(
                        api,
                        current_ops,
                        current_meta,
                        current_paths,
                        uploaded_files,
                        writer,
                        csvfile,
                    )
                    current_ops = []
                    current_meta = []
                    current_paths = []

            except Exception as e:
                print(f"  ✗ Error preparing {file_path.name}: {e}")
                continue

        # Process remaining files
        if current_ops:
            process_batch(
                api,
                current_ops,
                current_meta,
                current_paths,
                uploaded_files,
                writer,
                csvfile,
            )

    print("\nBatch processing complete!")


if __name__ == "__main__":
    main()
