from dolphain.catalog import build_catalog
from dolphain.io import getData, FS
import datetime
import numpy as np
import pandas as pd

def test_get_data():
    # 1. Build a mini catalog
    # We know where the files are from previous test
    target_dir = "datasets/ColorSynth/GoMRI-17/2017_South/BUOY200"
    print("Building mini catalog...")
    # Note: build_catalog returns a dataframe with datetime objects
    df = build_catalog(output_file="test_catalog.csv", path_pattern=f"{target_dir}/*.200")
    
    if df.empty:
        print("Failed to build catalog.")
        return
        
    print(f"Catalog built with {len(df)} records.")
    # Ensure timestamps are datetime objects (build_catalog returns them as such, but let's be safe)
    print(df[["filename", "start_time", "end_time"]].head())
    
    if len(df) < 2:
        print("Not enough files to test stitching.")
        return

    # 2. Pick a time range spanning two files
    # Let's take the end of the first file and start of the second
    first_file = df.iloc[0]
    
    # Start 5 seconds before end of first file
    start_time = first_file["end_time"] - datetime.timedelta(seconds=5)
    # Duration 10 seconds (so 5s from first, 5s from second)
    duration = 10.0
    
    print(f"Requesting data from {start_time} for {duration} seconds...")
    data = getData("test_source", start_time, duration, catalog_path="test_catalog.csv")
    
    print(f"Received data shape: {data.shape}")
    expected_samples = int(duration * FS)
    print(f"Expected samples: {expected_samples}")
    
    if len(data) == expected_samples:
        print("SUCCESS: Data length matches expected duration.")
    else:
        print(f"FAILURE: Data length mismatch. Got {len(data)}, expected {expected_samples}")
        
    # Check if data is not all zeros (it shouldn't be if files have content)
    if np.any(data):
        print("Data contains non-zero values.")
        print(f"Mean: {np.mean(data)}, Std: {np.std(data)}")
    else:
        print("WARNING: Data is all zeros.")

if __name__ == "__main__":
    test_get_data()
