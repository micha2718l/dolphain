#!/bin/bash
# Quick command to refresh showcase from CLICK_CHIRP_001
# Usage: ./refresh_from_chirp_click.sh

cd "$(dirname "$0")"
source .venv/bin/activate
python scripts/refresh_showcase.py --results-dir CLICK_CHIRP_001 --top 15
