# 💾 Data Management Guide

This guide explains how to manage the EARS data used by Dolphain, including uploading new data to HuggingFace and updating the built-in catalog.

## 🌍 Overview

Dolphain uses a hybrid data approach:

1.  **HuggingFace Hub**: Stores the actual binary EARS files (.130, .190, etc.) in the `ColorSynth/GoMRI-17` dataset.
2.  **Local Catalog**: A CSV file (`dolphain/data/default_catalog.csv`) distributed with the library that indexes available files.

This allows users to query and access terabytes of data without downloading it all first.

## 🛠️ Management Tools

We provide scripts in the `scripts/` directory to automate data management.

### 1. Upload Random Data (Easiest)

To upload a random batch of files from the attached drive to HuggingFace:

```bash
./scripts/upload_random.sh --count 200
```

This script will:

1.  Check your HuggingFace authentication.
2.  Select 200 random files from the drive (excluding ones already in the catalog).
3.  **Smart Batching**: Uploads are grouped into commits of 50 files each to avoid rate limits and keep the git history clean.
4.  Update your local `dolphain/data/default_catalog.csv`.

### 2. Advanced Selection

For more control, you can use the Python scripts directly:

**Step 1: Parse Drive Listing** (Only needed once)

```bash
python3 scripts/parse_drive_listing.py
```

Generates `ears_files_list.txt` from the drive listing file.

**Step 2: Prepare Batch**

```bash
# Select 500 random files
python3 scripts/prepare_upload_batch.py --random --count 500

# Select 100 files from a specific buoy
python3 scripts/prepare_upload_batch.py --buoy Buoy150 --count 100
```

Generates `upload_batch.json`.

**Step 3: Execute Upload**

```bash
python3 scripts/upload_batch.py
```

Uploads files in `upload_batch.json` and updates the catalog.

## 🔄 Workflow for Adding Data

1.  **Connect Drive**: Ensure the data drive is mounted at `/Volumes/ladcuno8tb0`.
2.  **Run Upload**: Use `./scripts/upload_random.sh` to upload a new batch.
3.  **Verify**: Check `dolphain/data/default_catalog.csv` to see new entries.
4.  **Commit**: Commit the updated catalog to git.

```bash
git add dolphain/data/default_catalog.csv
git commit -m "data: Add 200 new files from Buoy150 to catalog"
git push
```

## 📋 Catalog Structure

The catalog CSV contains:

- `file_path`: Path in HuggingFace (e.g., `datasets/ColorSynth/GoMRI-17/...`)
- `filename`: Original filename (e.g., `7178E5DC.200`)
- `start_time`: UTC timestamp of recording start
- `end_time`: UTC timestamp of recording end
- `duration`: Duration in seconds
- `size`: File size in bytes
- `n_samples`: Number of audio samples

## 🔐 Authentication

You need write access to the `ColorSynth/GoMRI-17` dataset.

1.  Get a token from [HuggingFace Settings](https://huggingface.co/settings/tokens).
2.  Login via CLI:
    ```bash
    huggingface-cli login
    ```
