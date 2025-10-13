#!/usr/bin/env python3
"""
Refresh the showcase with top files from a quick_find run.

This script:
1. Cleans out the current showcase directory
2. Reads top N files from a quick_find results directory
3. Generates a new showcase with those files

Usage:
    python refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15
    python refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 20 --output site/showcase_v2
"""

import sys
import argparse
import json
import shutil
from pathlib import Path
import subprocess

sys.path.insert(0, str(Path(__file__).parent))
import dolphain


def clean_showcase_dir(showcase_dir):
    """Remove all files from showcase directory except index.html."""
    showcase_dir = Path(showcase_dir)

    if not showcase_dir.exists():
        print(f"  ℹ️  Showcase directory doesn't exist: {showcase_dir}")
        return

    print(f"  🧹 Cleaning showcase directory: {showcase_dir}")

    # Remove subdirectories
    for subdir in ["audio", "images", "data"]:
        subdir_path = showcase_dir / subdir
        if subdir_path.exists():
            shutil.rmtree(subdir_path)
            print(f"     Removed: {subdir}/")

    # Remove JSON files but keep index.html
    for json_file in showcase_dir.glob("*.json"):
        json_file.unlink()
        print(f"     Removed: {json_file.name}")

    print(f"  ✓ Showcase cleaned")


def refresh_showcase(results_dir, top_n=15, output_dir="site/showcase"):
    """
    Refresh showcase with top N files from quick_find results.

    Args:
        results_dir: Directory containing quick_find results (e.g., CLICK_CHIRP_001)
        top_n: Number of top files to include in showcase
        output_dir: Showcase output directory
    """
    results_dir = Path(results_dir)
    output_dir = Path(output_dir)

    print("=" * 80)
    print("🎨 REFRESH SHOWCASE")
    print("=" * 80)
    print(f"Results directory: {results_dir}")
    print(f"Top files: {top_n}")
    print(f"Output directory: {output_dir}")
    print()

    # Step 1: Load results
    print("📋 Step 1: Loading results...")
    results_file = results_dir / "results.json"
    checkpoint_file = results_dir / "checkpoint.json"

    # Try results.json first (final results)
    if results_file.exists():
        print(f"  Loading final results: {results_file}")
        with open(results_file, "r") as f:
            data = json.load(f)
        results = data.get("results", [])
        print(f"  ✓ Loaded {len(results)} results (complete run)")

    # Fall back to checkpoint.json if results.json doesn't exist
    elif checkpoint_file.exists():
        print(f"  ⚠️  Final results not found, using checkpoint: {checkpoint_file}")
        print(f"     (Analysis appears to be in progress)")
        with open(checkpoint_file, "r") as f:
            data = json.load(f)
        results = data.get("results", [])
        print(f"  ✓ Loaded {len(results)} results so far (partial run)")

        # Sort by interestingness_score (checkpoint may not be sorted)
        results = sorted(
            results, key=lambda x: x.get("interestingness_score", 0), reverse=True
        )
        print(f"  ✓ Sorted by interestingness score")

    else:
        print(f"  ❌ Error: results.json not found in {results_dir}")
        print(f"     Is quick_find still running? Wait for it to complete.")
        return False

    if len(results) == 0:
        print(f"  ❌ No results found!")
        return False

    print(f"  Selected top {min(top_n, len(results))} files to showcase")
    print()

    # Step 2: Clean showcase
    print("🧹 Step 2: Cleaning showcase directory...")
    clean_showcase_dir(output_dir)
    print()

    # Step 3: Generate showcase
    print("🎬 Step 3: Generating showcase...")
    print(f"  Running generate_showcase.py...")

    # Determine which file to use for showcase generation
    if results_file.exists():
        checkpoint_path = results_file
    else:
        checkpoint_path = checkpoint_file

    # Build command - generate_showcase.py expects a checkpoint JSON file
    cmd = [
        sys.executable,
        "scripts/generate_showcase.py",
        "--checkpoint",
        str(checkpoint_path),
        "--top",
        str(top_n),
        "--output-dir",
        str(output_dir),
    ]

    # Run showcase generation
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ❌ Showcase generation failed!")
        print(result.stderr)
        return False

    print(result.stdout)

    # Step 4: Convert to MP3
    print("🎵 Step 4: Converting audio to MP3...")
    mp3_cmd = [
        sys.executable,
        "scripts/convert_to_mp3.py",
        "--showcase-dir",
        str(output_dir),
    ]

    result = subprocess.run(mp3_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ⚠️  MP3 conversion had issues (may be okay):")
        print(result.stderr)
    else:
        print(f"  ✓ MP3 conversion complete")

    print()
    print("=" * 80)
    print("✅ SHOWCASE REFRESH COMPLETE!")
    print("=" * 80)
    print(f"Showcase directory: {output_dir}/")
    print(f"\nTo view:")
    print(f"  cd site && python3 -m http.server 8000")
    print(f"  Then open: http://localhost:8000/showcase.html")
    print("=" * 80)

    return True

    # Step 5: Convert to MP3
    print("🎵 Step 5: Converting audio to MP3...")
    mp3_cmd = [
        sys.executable,
        "scripts/convert_to_mp3.py",
        "--showcase-dir",
        str(output_dir),
    ]

    result = subprocess.run(mp3_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  ⚠️  MP3 conversion had issues (may be okay):")
        print(result.stderr)
    else:
        print(f"  ✓ MP3 conversion complete")

    print()

    # Step 6: Summary
    print("=" * 80)
    print("✅ SHOWCASE REFRESH COMPLETE!")
    print("=" * 80)

    # Create a metadata file about this showcase
    metadata = {
        "source": str(results_dir),
        "top_n": top_n,
        "generated_from": "refresh_showcase.py",
        "detection_type": data.get("detection_targets", ["chirps", "click_trains"]),
        "n_analyzed": data.get("n_analyzed", len(results)),
        "files": [
            {
                "rank": i + 1,
                "filename": r["filename"],
                "score": r["interestingness_score"],
                "n_chirps": r.get("n_chirps", 0),
                "n_click_trains": r.get("n_click_trains", 0),
                "total_clicks": r.get("total_clicks", 0),
            }
            for i, r in enumerate(top_files)
        ],
    }

    metadata_file = output_dir / "showcase_metadata.json"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nShowcase created at: {output_dir}/")
    print(f"Metadata saved to: {metadata_file}")
    print(f"\nTop 5 files in showcase:")
    for i, r in enumerate(top_files[:5], 1):
        score = r["interestingness_score"]
        chirps = r.get("n_chirps", 0)
        clicks = r.get("total_clicks", 0)
        print(
            f"  {i}. {r['filename']} - Score: {score:.1f} (Chirps: {chirps}, Clicks: {clicks})"
        )

    print(f"\nTo view:")
    print(f"  cd site && python3 -m http.server 8000")
    print(f"  Then open: http://localhost:8000/showcase.html")

    # Clean up temp directory if used
    if copy_files and Path("temp_showcase_files").exists():
        print(f"\n🧹 Cleaning up temp files...")
        shutil.rmtree("temp_showcase_files")
        print(f"  ✓ Removed temp_showcase_files/")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Refresh showcase with top files from quick_find results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Refresh with top 15 from CLICK_CHIRP_001
  python refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15
  
  # Refresh with top 20, custom output
  python refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 20 --output site/showcase_v2
  
  # Don't copy files (use paths directly - faster but requires drive mounted)
  python refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15 --no-copy
  
Note: This will delete all files in the showcase directory before regenerating!
        """,
    )

    parser.add_argument(
        "--results-dir",
        type=Path,
        required=True,
        help="Directory containing quick_find results (e.g., CLICK_CHIRP_001)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=15,
        help="Number of top files to include (default: 15)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default="site/showcase",
        help="Showcase output directory (default: site/showcase)",
    )

    args = parser.parse_args()

    # Validate
    if not args.results_dir.exists():
        print(f"❌ Error: Results directory not found: {args.results_dir}")
        print(f"   Make sure quick_find has been run and completed.")
        sys.exit(1)

    # Check for results.json or checkpoint.json
    results_file = args.results_dir / "results.json"
    checkpoint_file = args.results_dir / "checkpoint.json"

    if not results_file.exists() and not checkpoint_file.exists():
        print(f"❌ Error: No results found in {args.results_dir}")
        print(f"   Neither results.json nor checkpoint.json exists.")
        print(f"   Has quick_find been started yet?")
        sys.exit(1)

    if not results_file.exists():
        print(f"⚠️  Using checkpoint data (analysis in progress)")
        print(f"   Will use top {args.top} files from checkpoint.json")
        print()

    # Run
    success = refresh_showcase(
        results_dir=args.results_dir, top_n=args.top, output_dir=args.output
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
