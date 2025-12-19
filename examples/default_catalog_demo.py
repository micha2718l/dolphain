"""
Example: Using the Built-in Default Catalog

This example demonstrates how to use Dolphain's built-in catalog
without any setup or file downloads.
"""

from dolphain.catalog import Catalog
import pandas as pd

print("=" * 70)
print("Dolphain Built-in Catalog Example")
print("=" * 70)
print()

# 1. Load the default catalog (no arguments needed!)
print("1. Loading built-in catalog...")
catalog = Catalog()
print(f"   ✓ Loaded {len(catalog.df)} files")
print(
    f"   Time range: {catalog.df['start_time'].min()} to {catalog.df['end_time'].max()}"
)
print()

# 2. View the catalog structure
print("2. Catalog structure:")
print(f"   Columns: {list(catalog.df.columns)}")
print()

# 3. Show first few entries
print("3. First 5 files:")
print(catalog.df.head()[["filename", "start_time", "duration"]])
print()

# 4. Query for a specific time range
print("4. Querying for files in a specific time range...")
start = pd.to_datetime("2017-06-28 00:30:00")
end = pd.to_datetime("2017-06-28 01:00:00")
files = catalog.query(start, end)
print(f"   ✓ Found {len(files)} files between {start} and {end}")
print()

# 5. Show file statistics
print("5. Catalog statistics:")
total_duration = catalog.df["duration"].sum()
total_size_gb = catalog.df["size"].sum() / (1024**3)
print(
    f"   Total duration: {total_duration:.2f} seconds ({total_duration/3600:.2f} hours)"
)
print(f"   Total size: {total_size_gb:.2f} GB")
print(f"   Average file size: {catalog.df['size'].mean()/(1024**2):.2f} MB")
print()

# 6. Find files in a specific hour
print("6. Finding all files in the first hour (00:20-01:20):")
hour_start = pd.to_datetime("2017-06-28 00:20:00")
hour_end = pd.to_datetime("2017-06-28 01:20:00")
hour_files = catalog.query(hour_start, hour_end)
print(f"   ✓ Found {len(hour_files)} files")
print(
    f"   First file: {hour_files.iloc[0]['filename']} at {hour_files.iloc[0]['start_time']}"
)
print(
    f"   Last file: {hour_files.iloc[-1]['filename']} at {hour_files.iloc[-1]['start_time']}"
)
print()

print("=" * 70)
print("Note: You can also load your own catalog by passing a path:")
print("  custom_catalog = Catalog('path/to/your/catalog.csv')")
print("=" * 70)
