#!/usr/bin/env python3
"""
Crawl through a data drive and catalog EARS files with progress persistence.

Usage:
    python crawl_data_drive.py [--resume]

Features:
- Counts files by directory
- Identifies EARS files (.210, .211, etc.)
- Saves progress periodically (every 100 directories)
- Can resume from last checkpoint
- Generates summary report
"""

import os
import sys
import json
import time
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Configuration
ROOT_DIR = Path("/Volumes/ladcuno8tb0/")
PROGRESS_FILE = Path("crawl_progress.json")
RESULTS_FILE = Path("data_drive_catalog.json")
REPORT_FILE = Path("data_drive_report.txt")


# EARS files have 3-digit extensions
def is_ears_file(filename):
    """Check if a file is an EARS file (has 3-digit extension)."""
    ext = Path(filename).suffix.lower()
    return len(ext) == 4 and ext[0] == "." and ext[1:].isdigit()


class DriveCrawler:
    def __init__(self, root_dir, resume=False):
        self.root_dir = Path(root_dir)
        self.resume = resume

        # Data structures
        self.catalog = defaultdict(
            lambda: {
                "total_files": 0,
                "ears_files": 0,
                "other_files": 0,
                "subdirs": 0,
                "ears_by_ext": defaultdict(int),
                "size_bytes": 0,
            }
        )

        self.processed_dirs = set()
        self.start_time = time.time()
        self.last_save_time = time.time()
        self.save_interval = 60  # Save every 60 seconds

        # Load progress if resuming
        if resume and PROGRESS_FILE.exists():
            self.load_progress()
            print(
                f"✓ Resuming from checkpoint: {len(self.processed_dirs)} directories already processed"
            )
        else:
            print(f"✓ Starting fresh crawl of {self.root_dir}")

    def load_progress(self):
        """Load progress from checkpoint file."""
        try:
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
                self.processed_dirs = set(data.get("processed_dirs", []))
                # Convert defaultdict structure back
                for path, stats in data.get("catalog", {}).items():
                    self.catalog[path] = {
                        "total_files": stats["total_files"],
                        "ears_files": stats["ears_files"],
                        "other_files": stats["other_files"],
                        "subdirs": stats["subdirs"],
                        "ears_by_ext": defaultdict(int, stats["ears_by_ext"]),
                        "size_bytes": stats["size_bytes"],
                    }
        except Exception as e:
            print(f"⚠️  Error loading progress: {e}")
            print("   Starting fresh...")

    def save_progress(self):
        """Save current progress to checkpoint file."""
        try:
            # Convert defaultdict to regular dict for JSON
            catalog_json = {}
            for path, stats in self.catalog.items():
                catalog_json[path] = {
                    "total_files": stats["total_files"],
                    "ears_files": stats["ears_files"],
                    "other_files": stats["other_files"],
                    "subdirs": stats["subdirs"],
                    "ears_by_ext": dict(stats["ears_by_ext"]),
                    "size_bytes": stats["size_bytes"],
                }

            progress_data = {
                "processed_dirs": list(self.processed_dirs),
                "catalog": catalog_json,
                "last_update": datetime.now().isoformat(),
                "total_dirs_processed": len(self.processed_dirs),
            }

            with open(PROGRESS_FILE, "w") as f:
                json.dump(progress_data, f, indent=2)

            self.last_save_time = time.time()
        except Exception as e:
            print(f"⚠️  Error saving progress: {e}")

    def should_save(self):
        """Check if it's time to save progress."""
        return (time.time() - self.last_save_time) > self.save_interval

    def crawl(self):
        """Crawl through the directory tree."""
        print(f"\n🔍 Crawling {self.root_dir}...")
        print(f"   Press Ctrl+C to pause (progress will be saved)\n")

        dirs_processed = 0

        try:
            for root, dirs, files in os.walk(self.root_dir):
                root_path = Path(root)
                rel_path = str(root_path.relative_to(self.root_dir))

                # Skip if already processed
                if rel_path in self.processed_dirs:
                    continue

                # Process this directory
                stats = self.catalog[rel_path]
                stats["subdirs"] = len(dirs)
                stats["total_files"] = len(files)

                # Analyze files
                for filename in files:
                    file_path = root_path / filename
                    ext = file_path.suffix.lower()

                    # Get file size (handle errors gracefully)
                    try:
                        size = file_path.stat().st_size
                        stats["size_bytes"] += size
                    except (OSError, PermissionError):
                        pass

                    # Check if it's an EARS file
                    if is_ears_file(filename):
                        stats["ears_files"] += 1
                        stats["ears_by_ext"][ext] += 1
                    else:
                        stats["other_files"] += 1

                # Mark as processed
                self.processed_dirs.add(rel_path)
                dirs_processed += 1

                # Progress update
                if dirs_processed % 10 == 0:
                    elapsed = time.time() - self.start_time
                    print(
                        f"\r  Processed: {len(self.processed_dirs)} dirs, "
                        f"{sum(s['total_files'] for s in self.catalog.values())} files, "
                        f"Time: {elapsed:.1f}s",
                        end="",
                        flush=True,
                    )

                # Periodic save
                if self.should_save():
                    print(f"\n  💾 Saving checkpoint...", end="", flush=True)
                    self.save_progress()
                    print(" done")

        except KeyboardInterrupt:
            print("\n\n⏸️  Paused by user")
            self.save_progress()
            print(f"✓ Progress saved to {PROGRESS_FILE}")
            print(f"  Resume with: python {sys.argv[0]} --resume")
            sys.exit(0)

        except Exception as e:
            print(f"\n\n❌ Error during crawl: {e}")
            self.save_progress()
            print(f"✓ Progress saved to {PROGRESS_FILE}")
            raise

        # Final save
        print("\n\n💾 Saving final results...")
        self.save_progress()
        self.save_results()
        self.generate_report()

        print(f"\n✅ Crawl complete!")
        print(f"   Results: {RESULTS_FILE}")
        print(f"   Report: {REPORT_FILE}")

    def save_results(self):
        """Save final results to JSON."""
        # Convert to regular dict
        catalog_json = {}
        for path, stats in self.catalog.items():
            catalog_json[path] = {
                "total_files": stats["total_files"],
                "ears_files": stats["ears_files"],
                "other_files": stats["other_files"],
                "subdirs": stats["subdirs"],
                "ears_by_ext": dict(stats["ears_by_ext"]),
                "size_bytes": stats["size_bytes"],
                "size_mb": round(stats["size_bytes"] / (1024 * 1024), 2),
            }

        results = {
            "root_directory": str(self.root_dir),
            "crawl_date": datetime.now().isoformat(),
            "total_directories": len(self.catalog),
            "catalog": catalog_json,
        }

        with open(RESULTS_FILE, "w") as f:
            json.dump(results, f, indent=2)

    def generate_report(self):
        """Generate human-readable text report."""
        with open(REPORT_FILE, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("DATA DRIVE CATALOG REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Root Directory: {self.root_dir}\n")
            f.write(f"Crawl Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Elapsed Time: {time.time() - self.start_time:.1f} seconds\n")
            f.write("\n")

            # Overall statistics
            total_dirs = len(self.catalog)
            total_files = sum(s["total_files"] for s in self.catalog.values())
            total_ears = sum(s["ears_files"] for s in self.catalog.values())
            total_other = sum(s["other_files"] for s in self.catalog.values())
            total_size = sum(s["size_bytes"] for s in self.catalog.values())

            f.write("OVERALL STATISTICS\n")
            f.write("-" * 80 + "\n")
            f.write(f"Total Directories:  {total_dirs:,}\n")
            f.write(f"Total Files:        {total_files:,}\n")
            f.write(
                f"  EARS Files:       {total_ears:,} ({100*total_ears/max(total_files,1):.1f}%)\n"
            )
            f.write(
                f"  Other Files:      {total_other:,} ({100*total_other/max(total_files,1):.1f}%)\n"
            )
            f.write(f"Total Size:         {total_size / (1024**3):.2f} GB\n")
            f.write("\n")

            # EARS files by extension
            ears_by_ext = defaultdict(int)
            for stats in self.catalog.values():
                for ext, count in stats["ears_by_ext"].items():
                    ears_by_ext[ext] += count

            if ears_by_ext:
                f.write("EARS FILES BY EXTENSION\n")
                f.write("-" * 80 + "\n")
                for ext in sorted(ears_by_ext.keys()):
                    count = ears_by_ext[ext]
                    f.write(f"  {ext:8s}  {count:,} files\n")
                f.write("\n")

            # Top directories by EARS file count
            f.write("TOP 20 DIRECTORIES BY EARS FILE COUNT\n")
            f.write("-" * 80 + "\n")
            sorted_dirs = sorted(
                self.catalog.items(), key=lambda x: x[1]["ears_files"], reverse=True
            )[:20]
            for path, stats in sorted_dirs:
                if stats["ears_files"] > 0:
                    f.write(f"  {stats['ears_files']:6,} files  {path}\n")
            f.write("\n")

            # Top directories by size
            f.write("TOP 20 DIRECTORIES BY SIZE\n")
            f.write("-" * 80 + "\n")
            sorted_dirs = sorted(
                self.catalog.items(), key=lambda x: x[1]["size_bytes"], reverse=True
            )[:20]
            for path, stats in sorted_dirs:
                size_gb = stats["size_bytes"] / (1024**3)
                f.write(f"  {size_gb:8.2f} GB  {path}\n")
            f.write("\n")

            # Directory tree (first level only)
            f.write("DIRECTORY STRUCTURE (TOP LEVEL)\n")
            f.write("-" * 80 + "\n")
            top_level = [
                path for path in self.catalog.keys() if "/" not in path.strip("./")
            ]
            for path in sorted(top_level):
                stats = self.catalog[path]
                f.write(
                    f"  {path or '.':<40s}  {stats['total_files']:6,} files  "
                    f"{stats['subdirs']:4,} subdirs  "
                    f"{stats['size_bytes']/(1024**2):8.1f} MB\n"
                )


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Crawl data drive and catalog EARS files"
    )
    parser.add_argument(
        "--resume", action="store_true", help="Resume from last checkpoint"
    )
    args = parser.parse_args()

    # Check if root directory exists
    if not ROOT_DIR.exists():
        print(f"❌ Error: Root directory not found: {ROOT_DIR}")
        print(f"   Is the drive mounted?")
        sys.exit(1)

    # Create crawler and start
    crawler = DriveCrawler(ROOT_DIR, resume=args.resume)
    crawler.crawl()


if __name__ == "__main__":
    main()
