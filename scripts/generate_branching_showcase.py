#!/usr/bin/env python3
"""Generate the branching showcase data structure for the hackathon explorer.

Usage example:
    python scripts/generate_branching_showcase.py \
        --showcase-data site/showcase/showcase_data.json \
        --output-dir site/branch_explorer
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

# Ensure local package imports work when executed as a script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dolphain.branching import build_branch_tree  # noqa: E402


def _load_showcase_data(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Showcase data file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    if "files" not in payload:
        raise KeyError(
            "Showcase data missing 'files' key. Did the generator change its output?"
        )

    return payload


def generate_branching_data(showcase_path: Path, output_dir: Path) -> Path:
    """Build the branching tree and persist it as JSON."""

    showcase_payload = _load_showcase_data(showcase_path)
    tree = build_branch_tree(showcase_payload["files"])

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "branching_data.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)

    return output_path


def main(argv: Any = None) -> None:
    parser = argparse.ArgumentParser(
        description="Generate a branching showcase JSON tree from the main showcase dataset.",
    )
    parser.add_argument(
        "--showcase-data",
        type=Path,
        default=Path("site/showcase/showcase_data.json"),
        help="Path to the existing showcase_data.json file",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("site/branch_explorer"),
        help="Directory to write branching_data.json",
    )

    args = parser.parse_args(argv)

    output_path = generate_branching_data(args.showcase_data, args.output_dir)

    print("🌿 Dolphin Branch Explorer data generated!")
    print(f"   Source : {args.showcase_data}")
    print(f"   Output : {output_path}")
    print("\nNext steps:")
    print("  1. Open site/branch_explorer/index.html in a browser")
    print("  2. Follow the branching paths and enjoy the sonic adventure 🐬")


if __name__ == "__main__":
    main()
