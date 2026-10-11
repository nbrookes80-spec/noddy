#!/bin/bash
# start_avatarify_aws.sh - Avatarify launcher with AWS EC2 proxy support
# Usage: ./start_avatarify_aws.sh /path/to/video.mp4 [AWS_HOST] [INPUT_PORT] [OUTPUT_PORT]
# Example: ./start_avatarify_aws.sh ~/Videos/test.mp4 13.210.132.155 5557 5558

set -e  # Exit on error

# Configuration
AVATARIFY_DIR="$HOME/Downloads/avatarify-python-master"
VENV_PATH="$AVATARIFY_DIR/venv"

# Parameters with defaults
VIDEO_FILE="${1:?Usage: $0 /path/to/video.mp4 [AWS_HOST] [INPUT_PORT] [OUTPUT_PORT]}"
AWS_HOST="${2:-13.210.132.155}"
INPUT_PORT="${3:-5557}"
OUTPUT_PORT="${4:-5558}"

echo "=================================="
echo "Avatarify AWS Launcher"
echo "=================================="
echo ""

# Validate video file exists
if [ ! -f "$VIDEO_FILE" ]; then
    echo "ERROR: Video file not found: $VIDEO_FILE"
    exit 1
fi

# Validate virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    echo "Please run setup_avatarify_aws.sh first."
    exit 1
fi

echo "Configuration:"
echo "  Video file: $VIDEO_FILE"
echo "  AWS host: $AWS_HOST"
echo "  Input port: $INPUT_PORT"
echo "  Output port: $OUTPUT_PORT"
echo ""

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "ERROR: ffmpeg not found. Install with: sudo apt install ffmpeg"
    exit 1
fi

# Get video properties
echo "Analyzing video file..."
VIDEO_INFO=$(ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,codec_name,pix_fmt \
  -of csv=p=0 "$VIDEO_FILE")

IFS=',' read -r WIDTH HEIGHT FPS CODEC PIXFMT <<< "$VIDEO_INFO"

# Clean up frame rate (e.g., "30000/1001" -> use FFmpeg's default scaling)
echo "  Resolution: ${WIDTH}x${HEIGHT}"
echo "  Frame rate: $FPS"
echo "  Codec: $CODEC"
echo "  Pixel format: $PIXFMT"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"
echo "✓ Virtual environment activated"
echo ""

# Build ffmpeg command
# Convert video to: 512x512 resolution, RGB24 format, 30fps
echo "Preparing video stream..."
echo "  Target: 512x512, RGB24, 30fps"
echo ""

# Check if TCP proxy is reachable
echo "Testing connection to AWS proxy ($AWS_HOST:$INPUT_PORT)..."
if timeout 2 bash -c "cat < /dev/null > /dev/tcp/$AWS_HOST/$INPUT_PORT" 2>/dev/null; then
    echo "✓ AWS proxy is reachable"
else
    echo "WARNING: AWS proxy at $AWS_HOST:$INPUT_PORT is not reachable"
    echo "Make sure your AWS EC2 instance is running and the reverse SSH tunnel is active."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "=================================="
echo "Starting Avatarify Client..."
echo "=================================="
echo ""

# Start ffmpeg piping video to Avatarify client
# ffmpeg converts video to raw RGB24 at 512x512, 30fps
# Output is piped to client stdin
ffmpeg -i "$VIDEO_FILE" \
  -vf "scale=512:512,fps=30" \
  -pix_fmt rgb24 \
  -f rawvideo \
  -loglevel warning \
  pipe: | \
python3 "$AVATARIFY_DIR/run.py" \
  --input tcp://$AWS_HOST:$INPUT_PORT \
  --output tcp://$AWS_HOST:$OUTPUT_PORT \
  --checkpoint-dir "$AVATARIFY_DIR/checkpoints"

# Cleanup happens automatically when ffmpeg/client exit
echo ""
echo "Avatarify session ended."
