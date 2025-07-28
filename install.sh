#!/bin/bash
# Installation script to avoid dependency conflicts

set -e

echo "Installing FastAPI app dependencies..."
echo "This script addresses the pandas/numpy dependency conflict from PR #68"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install with no-deps first to avoid dependency resolution conflicts
echo "Installing core dependencies..."
pip install --no-deps fastapi==0.114.0
pip install --no-deps uvicorn==0.30.0  
pip install --no-deps gunicorn==22.0.0

# Then install required dependencies
echo "Installing FastAPI dependencies..."
pip install starlette pydantic typing-extensions httpx anyio sniffio idna

# Install optional dependencies that FastAPI commonly uses
echo "Installing optional FastAPI dependencies..."
pip install jinja2 python-multipart orjson ujson

# Install uvicorn[standard] dependencies
echo "Installing server dependencies..."
pip install uvloop httptools websockets watchfiles click

# Install remaining utilities
pip install email-validator

echo "Installation complete!"
echo "Verifying no pandas/numpy dependencies..."
python -c "
import subprocess
import sys
result = subprocess.run([sys.executable, '-m', 'pip', 'list'], capture_output=True, text=True)
packages = result.stdout.lower()
if 'pandas' in packages:
    print('ERROR: pandas found in dependencies!')
    sys.exit(1)
if 'numpy' in packages:
    print('ERROR: numpy found in dependencies!')
    sys.exit(1)
print('✓ No unwanted pandas/numpy dependencies found')
"