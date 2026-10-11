#!/bin/bash
# setup_avatarify_aws.sh - One-time setup script for Avatarify AWS environment
# Usage: ./setup_avatarify_aws.sh
# This script creates a Python 3.12 virtual environment and installs all required dependencies

set -e  # Exit on any error

AVATARIFY_DIR="$HOME/Downloads/avatarify-python-master"
VENV_PATH="$AVATARIFY_DIR/venv"

echo "=================================="
echo "Avatarify AWS Setup Script"
echo "=================================="
echo ""

# Check if Avatarify directory exists
if [ ! -d "$AVATARIFY_DIR" ]; then
    echo "ERROR: Avatarify directory not found at $AVATARIFY_DIR"
    echo "Please extract the Avatarify archive first."
    exit 1
fi

# Check if Python 3.12 is available
if ! command -v python3.12 &> /dev/null; then
    echo "ERROR: python3.12 not found. Please install Python 3.12 first."
    exit 1
fi

echo "Step 1: Creating Python 3.12 virtual environment..."
if [ -d "$VENV_PATH" ]; then
    echo "Virtual environment already exists at $VENV_PATH"
    read -p "Remove and recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$VENV_PATH"
        python3.12 -m venv "$VENV_PATH"
        echo "✓ Virtual environment recreated"
    else
        echo "Using existing virtual environment"
    fi
else
    python3.12 -m venv "$VENV_PATH"
    echo "✓ Virtual environment created"
fi

echo ""
echo "Step 2: Activating virtual environment..."
source "$VENV_PATH/bin/activate"
echo "✓ Virtual environment activated"

echo ""
echo "Step 3: Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip, setuptools, and wheel upgraded"

echo ""
echo "Step 4: Installing required Python packages..."
echo "This may take a few minutes..."

# Install packages without pinned versions for Python 3.12 compatibility
PACKAGES=(
    "opencv-python"
    "opencv-contrib-python"
    "pyzmq"
    "msgpack_numpy"
    "pyyaml"
    "numpy"
    "pyfakewebcam"
    "requests"
    "scipy"
    "scikit-image"
    "pillow"
)

for package in "${PACKAGES[@]}"; do
    echo -n "  Installing $package... "
    pip install "$package" > /dev/null 2>&1
    echo "✓"
done

echo ""
echo "Step 5: Verifying installation..."
echo "Testing Python imports..."

python3 << 'EOF'
import sys
required_modules = [
    'cv2', 'zmq', 'msgpack_numpy', 'yaml', 'numpy', 'pyfakewebcam',
    'requests', 'scipy', 'skimage', 'PIL'
]

failed = []
for module in required_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        print(f"  ✗ {module} FAILED")
        failed.append(module)

if failed:
    print(f"\nERROR: {len(failed)} module(s) failed to import: {', '.join(failed)}")
    sys.exit(1)
EOF

echo ""
echo "=================================="
echo "✓ Setup Complete!"
echo "=================================="
echo ""
echo "Your Avatarify environment is ready to use."
echo "To start Avatarify with AWS proxy support, run:"
echo "  bash $AVATARIFY_DIR/start_avatarify_aws.sh"
echo ""
