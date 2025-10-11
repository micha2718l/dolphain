#!/usr/bin/env python3
"""
Command-line interface for Dolphain acoustic data file analysis.

Usage:
    python ears_cli.py <filepath> [--normalize] [--fmax FMAX]

Example:
    python ears_cli.py unophysics/sample_data/71621DC7.190 --fmax 5000
"""

import sys
import argparse
from pathlib import Path
import dolphain


def main():
    parser = argparse.ArgumentParser(
        description="Analyze EARS acoustic data files with Dolphain",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sample_data/71621DC7.190
  %(prog)s sample_data/71621DC7.190 --normalize --fmax 5000
  %(prog)s sample_data/71621DC7.190 --plot waveform
  %(prog)s sample_data/71621DC7.190 --plot spectrogram --fmax 8000
        """,
    )

    parser.add_argument(
        "filepath", type=str, help="Path to EARS data file (.130, .190, etc.)"
    )

    parser.add_argument(
        "--normalize", action="store_true", help="Normalize data to [-1, 1] range"
    )

    parser.add_argument(
        "--plot",
        type=str,
        choices=["waveform", "spectrogram", "overview", "all"],
        default="overview",
        help="Type of plot to generate (default: overview)",
    )

    parser.add_argument(
        "--fmax",
        type=float,
        default=None,
        help="Maximum frequency for spectrogram (Hz)",
    )

    parser.add_argument(
        "--xlim",
        type=float,
        nargs=2,
        metavar=("START", "END"),
        default=None,
        help="Time limits for waveform zoom (seconds)",
    )

    parser.add_argument(
        "--no-plot", action="store_true", help="Only print file info, do not show plots"
    )

    args = parser.parse_args()

    # Check if file exists
    filepath = Path(args.filepath)
    if not filepath.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return 1

    # Read the file
    print(f"Reading file: {filepath}")
    try:
        data = dolphain.read_ears_file(filepath, normalize=args.normalize)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 1

    # Print file information
    print("\n" + "=" * 60)
    dolphain.print_file_info(data, filepath)
    print("=" * 60 + "\n")

    if args.normalize:
        print("Data was normalized to [-1, 1] range\n")

    # Generate plots
    if not args.no_plot:
        print("Generating plots...")

        if args.plot == "waveform" or args.plot == "all":
            dolphain.plot_waveform(data, xlim=args.xlim)

        if args.plot == "spectrogram" or args.plot == "all":
            dolphain.plot_spectrogram(data, fmax=args.fmax)

        if args.plot == "overview" or args.plot == "all":
            dolphain.plot_overview(data, fmax=args.fmax, xlim_zoom=args.xlim)

    return 0


if __name__ == "__main__":
    sys.exit(main())
