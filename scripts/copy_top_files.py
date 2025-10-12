#!/usr/bin/env python3
"""
Copy top N files from analysis results to a local directory.

This is useful when the external drive is disconnected - copy the files
locally first, then generate the showcase from the local copies.
"""

import json
import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='Copy top files from analysis results')
    parser.add_argument('--checkpoint', required=True, help='Path to checkpoint JSON')
    parser.add_argument('--top', type=int, default=25, help='Number of top files to copy')
    parser.add_argument('--output-dir', default='temp_showcase_files', 
                       help='Directory to copy files to')
    
    args = parser.parse_args()
    
    # Load results
    print(f"📂 Loading results from {args.checkpoint}")
    with open(args.checkpoint, 'r') as f:
        results = json.load(f)
    
    # Get top files (handle both formats)
    if 'top_files' in results:
        top_files = results['top_files'][:args.top]
        file_list = [f['file'] for f in top_files]
    elif 'results' in results:
        sorted_results = sorted(results['results'], 
                               key=lambda x: x.get('interestingness_score', 0), 
                               reverse=True)
        file_list = [r['file'] for r in sorted_results[:args.top]]
    else:
        raise ValueError("Unknown results format")
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"🎯 Copying top {len(file_list)} files to {output_dir}/")
    print()
    
    # Copy files
    copied = 0
    missing = []
    
    for i, file_path in enumerate(file_list, 1):
        src = Path(file_path)
        
        if not src.exists():
            print(f"⚠️  Rank {i:2d}: {src.name} - FILE NOT FOUND (drive disconnected?)")
            missing.append(file_path)
            continue
        
        # Copy file
        dst = output_dir / src.name
        try:
            shutil.copy2(src, dst)
            file_size = dst.stat().st_size / 1024  # KB
            print(f"✅ Rank {i:2d}: {src.name} ({file_size:.1f} KB)")
            copied += 1
        except Exception as e:
            print(f"❌ Rank {i:2d}: {src.name} - ERROR: {e}")
            missing.append(file_path)
    
    print()
    print(f"✅ Copied {copied}/{len(file_list)} files successfully")
    
    if missing:
        print(f"⚠️  {len(missing)} files were not accessible")
        print(f"   Make sure the external drive is connected at:")
        print(f"   {Path(missing[0]).parent}")
    
    # Save a manifest file
    manifest = {
        'original_checkpoint': str(args.checkpoint),
        'files_requested': len(file_list),
        'files_copied': copied,
        'output_directory': str(output_dir),
        'copied_files': [str(output_dir / Path(f).name) for f in file_list if (output_dir / Path(f).name).exists()]
    }
    
    manifest_path = output_dir / 'manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"📝 Manifest saved to {manifest_path}")
    print()
    print("🚀 Next step: Run showcase generator on local files:")
    print(f"   python scripts/generate_showcase_local.py --input-dir {output_dir} --top {args.top}")


if __name__ == '__main__':
    main()
