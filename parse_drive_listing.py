#!/usr/bin/env python3
"""
Parse Windows drive listing and extract EARS file paths.
Converts Windows paths to macOS mount paths.
"""

import re
import sys
from pathlib import Path

def parse_drive_listing(listing_file: Path, mount_point: Path):
    """
    Parse the Windows drive listing and extract EARS file paths.
    
    Returns list of Path objects for EARS files.
    """
    ears_files = []
    current_dir = None
    
    with open(listing_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            # Look for directory markers
            if line.startswith("📁 Directory:"):
                # Extract directory path
                match = re.search(r'Directory: (.+)', line)
                if match:
                    dir_path = match.group(1).strip()
                    # Convert Windows path to Unix
                    if dir_path.startswith('D:'):
                        dir_path = dir_path[2:]  # Remove D:
                    dir_path = dir_path.replace('\\', '/')
                    if dir_path == '/':
                        current_dir = mount_point
                    else:
                        current_dir = mount_point / dir_path.lstrip('/')
            
            # Look for EARS files (3-digit extensions)
            elif line.strip().startswith("📄"):
                match = re.search(r'📄\s+([^\s]+\.[0-9]{3})', line)
                if match:
                    filename = match.group(1).strip()
                    if current_dir:
                        file_path = current_dir / filename
                        ears_files.append(file_path)
    
    return ears_files

if __name__ == '__main__':
    listing_file = Path("/Volumes/ladcuno8tb0/drive_listing_D_20251012_002749.txt")
    mount_point = Path("/Volumes/ladcuno8tb0")
    
    print("Parsing drive listing...")
    ears_files = parse_drive_listing(listing_file, mount_point)
    
    print(f"\nFound {len(ears_files)} EARS files")
    
    # Show sample
    print("\nFirst 10 files:")
    for f in ears_files[:10]:
        exists = "✓" if f.exists() else "✗"
        print(f"  {exists} {f}")
    
    # Save to file
    output_file = Path("ears_files_list.txt")
    with open(output_file, 'w') as f:
        for file_path in ears_files:
            f.write(str(file_path) + '\n')
    
    print(f"\n✓ Saved complete list to: {output_file}")
    print(f"  Total files: {len(ears_files)}")
