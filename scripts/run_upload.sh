#!/bin/bash
# Script to run the batch upload process

# Ensure we are in the project root
cd "$(dirname "$0")/.."

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

# Run upload
echo "Starting upload..."
.venv/bin/python3 scripts/upload_batch.py
