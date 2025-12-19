#!/bin/bash
# Script to select a random batch of files and upload them

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Default count
COUNT=200

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --count) COUNT="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "=== Dolphain Data Upload Tool ==="
echo "Preparing to upload $COUNT random files..."

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
fi

# Check if authenticated
.venv/bin/python3 scripts/check_auth.py > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Please login to HuggingFace first:"
    .venv/bin/hf auth login
fi

# 1. Prepare the batch
echo "Selecting files..."
.venv/bin/python3 scripts/prepare_upload_batch.py --random --count $COUNT

# 2. Run the upload
echo "Starting upload..."
.venv/bin/python3 scripts/upload_batch.py

echo "=== Upload Complete ==="
echo "Don't forget to commit the updated catalog!"
