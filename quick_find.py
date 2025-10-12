#!/usr/bin/env python3
"""
Quick-start script for finding interesting files in a hurry.

This is a simplified wrapper that runs the most common workflow:
1. Sample files from your drive
2. Find the most interesting ones
3. Generate a quick report

Usage:
    python quick_find.py /Volumes/ladcuno8tb0/
    
    # Custom sample size (default 1000 files)
    python quick_find.py /Volumes/ladcuno8tb0/ --n-files 500
"""

import sys
import argparse
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


def quick_find(data_dir: Path = None, file_list_path: Path = None, n_files: int = 1000, output_dir: Path = None):
    """
    Quick analysis to find top interesting files.
    
    Args:
        data_dir: Root directory to search (deprecated, use file_list_path)
        file_list_path: Path to pre-generated file list (one file per line)
        n_files: Number of files to sample
        output_dir: Where to save results
    """
    output_dir = output_dir or Path("quick_find_results")
    output_dir.mkdir(exist_ok=True)
    
    print("="*80)
    print("QUICK FIND - INTERESTING EARS FILES")
    print("="*80)
    print(f"Sample size: {n_files} files")
    print(f"Output: {output_dir}")
    print()
    
    # Step 1: Load file list
    print("Step 1: Loading EARS file list...")
    start_time = time.time()
    
    if file_list_path and file_list_path.exists():
        print(f"  Reading from: {file_list_path}")
        with open(file_list_path, 'r') as f:
            all_files = [Path(line.strip()) for line in f if line.strip()]
        print(f"  Loaded {len(all_files)} files from list")
    elif data_dir:
        print(f"  Scanning directory: {data_dir}")
        all_files = dolphain.find_data_files(data_dir, '**/*.[0-9][0-9][0-9]')
        print(f"  Found {len(all_files)} total EARS files")
    else:
        print("  ❌ Must provide either --file-list or --data-dir")
        return
    
    if len(all_files) == 0:
        print("  ❌ No EARS files found!")
        return
    
    # Sample if needed
    if len(all_files) > n_files:
        import random
        file_list = random.sample(all_files, n_files)
        print(f"  Sampling {n_files} files randomly")
    else:
        file_list = all_files
        print(f"  Using all {len(file_list)} files")
    
    print(f"  Time: {time.time() - start_time:.1f}s\n")
    
    # Step 2: Quick analysis
    print("Step 2: Running quick analysis...")
    start_time = time.time()
    
    # Use whistle detection pipeline - it's comprehensive
    pipeline = dolphain.WhistleDetectionPipeline(
        denoise=True,
        power_threshold_percentile=85.0,
        min_duration=0.1
    )
    
    results = []
    errors = []
    
    for i, file_path in enumerate(file_list):
        try:
            result = pipeline(file_path)
            result['file'] = str(file_path)
            result['filename'] = file_path.name
            
            # Calculate interestingness score
            score = 0.0
            n_whistles = result.get('n_whistles', 0)
            coverage = result.get('whistle_coverage_percent', 0)
            
            # Simple scoring
            score += min(50, n_whistles * 0.5)  # Whistles (max 50 pts)
            score += min(30, coverage * 0.3)     # Coverage (max 30 pts)
            score += 20 if n_whistles > 10 else 0  # Bonus for lots of activity
            
            result['interestingness_score'] = round(score, 2)
            results.append(result)
            
        except Exception as e:
            errors.append({'file': str(file_path), 'error': str(e)})
        
        # Progress
        if (i + 1) % 50 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (len(file_list) - i - 1) / rate
            print(f"  Progress: {i+1}/{len(file_list)} ({(i+1)/len(file_list)*100:.1f}%) "
                  f"- {rate:.1f} files/s - ETA: {remaining/60:.1f}m")
    
    print(f"  Completed {len(results)} files successfully")
    print(f"  Errors: {len(errors)}")
    print(f"  Time: {time.time() - start_time:.1f}s\n")
    
    # Step 3: Analyze and report
    print("Step 3: Generating report...")
    
    # Sort by interestingness
    results.sort(key=lambda x: x['interestingness_score'], reverse=True)
    
    # Save full results
    import json
    with open(output_dir / "results.json", 'w') as f:
        json.dump({
            'n_analyzed': len(results),
            'n_errors': len(errors),
            'results': results,
            'errors': errors
        }, f, indent=2)
    
    # Save top files list
    top_20 = results[:20]
    with open(output_dir / "top_20_files.txt", 'w') as f:
        f.write("TOP 20 MOST INTERESTING FILES\n")
        f.write("="*80 + "\n\n")
        f.write(f"{'Rank':<6} {'Score':<8} {'Whistles':<10} {'Coverage':<10} {'File'}\n")
        f.write("-"*80 + "\n")
        
        for i, result in enumerate(top_20, 1):
            score = result['interestingness_score']
            whistles = result.get('n_whistles', 0)
            coverage = result.get('whistle_coverage_percent', 0)
            filename = result['filename']
            
            f.write(f"{i:<6} {score:<8.1f} {whistles:<10} {coverage:<9.1f}% {filename}\n")
        
        f.write("\n\nFull file paths:\n")
        f.write("-"*80 + "\n")
        for i, result in enumerate(top_20, 1):
            f.write(f"{i}. {result['file']}\n")
    
    # Save CSV for analysis
    import pandas as pd
    df = pd.DataFrame(results)
    df.to_csv(output_dir / "all_results.csv", index=False)
    
    print(f"  ✓ Saved: {output_dir}/results.json")
    print(f"  ✓ Saved: {output_dir}/top_20_files.txt")
    print(f"  ✓ Saved: {output_dir}/all_results.csv")
    
    # Print summary
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    print(f"Files analyzed: {len(results)}")
    print(f"Files with whistles: {sum(1 for r in results if r.get('n_whistles', 0) > 0)}")
    print(f"Mean whistles per file: {sum(r.get('n_whistles', 0) for r in results) / len(results):.2f}")
    print()
    
    print("TOP 5 FILES:")
    for i, result in enumerate(results[:5], 1):
        score = result['interestingness_score']
        whistles = result.get('n_whistles', 0)
        coverage = result.get('whistle_coverage_percent', 0)
        print(f"  {i}. Score: {score:.1f} | Whistles: {whistles} | Coverage: {coverage:.1f}%")
        print(f"     {result['filename']}")
    
    print("\n" + "="*80)
    print("✅ QUICK FIND COMPLETE!")
    print("="*80)
    print(f"\nResults saved to: {output_dir}/")
    print(f"\nNext steps:")
    print(f"  1. Review top_20_files.txt")
    print(f"  2. Copy interesting files to working directory")
    print(f"  3. Run full analysis: python explore_interesting.py --results {output_dir}/results.json")


def main():
    parser = argparse.ArgumentParser(
        description='Quick find interesting EARS files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use pre-generated file list (RECOMMENDED - much faster!)
  python quick_find.py --file-list ears_files_list.txt --n-files 100
  
  # Scan directory (slow on external drives)
  python quick_find.py --data-dir /Volumes/ladcuno8tb0/ --n-files 500
  
  # Custom output location
  python quick_find.py --file-list ears_files_list.txt --output-dir my_results/
        """
    )
    
    parser.add_argument('--data-dir', type=Path,
                       help='Root directory containing EARS files (slow)')
    parser.add_argument('--file-list', type=Path,
                       help='Pre-generated file list (one file per line) - RECOMMENDED')
    parser.add_argument('--n-files', type=int, default=1000,
                       help='Number of files to sample (default: 1000)')
    parser.add_argument('--output-dir', type=Path,
                       help='Output directory (default: quick_find_results)')
    
    args = parser.parse_args()
    
    # Validate
    if not args.file_list and not args.data_dir:
        print("❌ Error: Must provide either --file-list or --data-dir")
        parser.print_help()
        sys.exit(1)
    
    if args.data_dir and not args.data_dir.exists():
        print(f"❌ Error: Directory not found: {args.data_dir}")
        print(f"   Is the drive mounted?")
        sys.exit(1)
    
    if args.file_list and not args.file_list.exists():
        print(f"❌ Error: File list not found: {args.file_list}")
        print(f"   Run: python parse_drive_listing.py")
        sys.exit(1)
    
    # Run
    quick_find(
        data_dir=args.data_dir,
        file_list_path=args.file_list,
        n_files=args.n_files,
        output_dir=args.output_dir
    )


if __name__ == '__main__':
    main()
