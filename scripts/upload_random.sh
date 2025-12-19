#!/bin/bash
# Script to select a random batch of files and upload them

# Ensure we are in the project root
cd "$(dirname "$0")/.."

# Default count
COUNT=200
RESUME=false
CONTIGUOUS=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --count) COUNT="$2"; shift ;;
        --resume) RESUME=true ;;
        --contiguous) CONTIGUOUS=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "=== Dolphain Data Upload Tool ==="

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

if [ "$RESUME" = true ]; then
    echo "Resuming previous batch..."
    if [ ! -f "upload_batch.json" ]; then
        echo "Error: No batch file found to resume. Run without --resume first."
        exit 1
    fi
else
    echo "Preparing to upload $COUNT files..."
    # 1. Prepare the batch
    echo "Selecting files..."
    if [ "$CONTIGUOUS" = true ]; then
        .venv/bin/python3 scripts/prepare_upload_batch.py --contiguous --count $COUNT
    else
        .venv/bin/python3 scripts/prepare_upload_batch.py --random --count $COUNT
    fi
fi

# 2. Run the upload
echo "Starting upload..."
if [ "$CONTIGUOUS" = true ]; then
    # Allow overwriting for contiguous blocks
    .venv/bin/python3 scripts/upload_batch.py --overwrite
else
    .venv/bin/python3 scripts/upload_batch.py
fi

echo "=== Upload Complete ==="
echo "Don't forget to commit the updated catalog!"
