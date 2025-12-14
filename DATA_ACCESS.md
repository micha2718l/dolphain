# 💾 Data Access Guide

**Last Updated:** December 13, 2025

Dolphain provides a powerful abstraction layer for accessing the massive EARS dataset hosted on HuggingFace. Instead of managing thousands of individual binary files, you can query data by **time range**.

---

## 🚀 Quick Start

```python
from dolphain import getData, build_catalog
import datetime

# 1. Build the catalog (run once)
# This scans the HuggingFace dataset and creates a local index
build_catalog()

# 2. Fetch data by time
start = datetime.datetime(2017, 6, 28, 0, 20, 51)
data = getData(source="GoMRI-17", start_time=start, length_seconds=10.0)

print(f"Got {len(data)} samples!")
```

---

## 📚 Core Concepts

### 1. The Catalog (`catalog.csv`)

The dataset consists of thousands of binary files (`.130`, `.190`, `.210`, etc.), each containing ~20 seconds of audio. To efficiently find data, we first build a **Catalog**.

- **Function:** `build_catalog(dataset_id, output_file, path_pattern)`
- **Output:** A CSV file containing `filename`, `start_time`, `end_time`, and `file_path` for every file in the dataset.
- **Performance:** Scanning the full dataset takes a few minutes. You only need to do this once.

### 2. Data Stitching (`getData`)

The `getData` function abstracts away file boundaries. If you request a 60-second chunk that spans 3 different files, `getData` will:

1. Query the catalog to find the 3 relevant files.
2. Calculate the byte offsets for the start and end of your requested segment.
3. Read only the necessary bytes from HuggingFace (using HTTP Range requests).
4. Stitch the arrays together into a single continuous NumPy array.

---

## 📖 API Reference

### `build_catalog`

Scans the HuggingFace repository and creates a local CSV index.

```python
def build_catalog(
    dataset_id="ColorSynth/GoMRI-17",
    output_file="catalog.csv",
    path_pattern=None
):
    ...
```

- **dataset_id**: The HuggingFace dataset ID.
- **output_file**: Where to save the CSV index.
- **path_pattern**: (Optional) A glob pattern to limit the scan (e.g., `"**/BUOY200/*.200"`). Useful for testing.

### `getData`

Retrieves acoustic data for a specific time range.

```python
def getData(
    source,
    start_time,
    length_seconds,
    catalog_path="catalog.csv"
):
    ...
```

- **source**: Dataset identifier (currently unused, reserved for future multi-dataset support).
- **start_time**: `datetime.datetime` object for the start of the audio.
- **length_seconds**: Duration in seconds (float).
- **catalog_path**: Path to the CSV index created by `build_catalog`.

---

## 💡 Advanced Usage

### Partial Cataloging

If you only care about a specific deployment (e.g., Buoy 200), you can save time by cataloging only that folder:

```python
build_catalog(
    output_file="buoy200_catalog.csv",
    path_pattern="datasets/ColorSynth/GoMRI-17/2017_South/BUOY200/*.200"
)
```

### Visualizing Stitched Data

See `examples/data_stitching_demo.ipynb` for a complete example of fetching and plotting stitched data.
