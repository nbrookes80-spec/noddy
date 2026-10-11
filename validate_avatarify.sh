#!/bin/bash
# validate_avatarify.sh - Comprehensive validation of Avatarify AWS setup
# Usage: bash validate_avatarify.sh

set -e

AVATARIFY_DIR="$HOME/Downloads/avatarify-python-master"
VENV_PATH="$AVATARIFY_DIR/venv"
VIDEO_FILE="/home/nathan/Videos/video GEN 01/VIDEO 0001.mp4"
REPORT_FILE="/tmp/avatarify_validation_report.txt"

echo "=============================================="
echo "Avatarify AWS Setup Validator"
echo "=============================================="
echo ""

# Initialize report
{
    echo "Avatarify AWS Setup Validation Report"
    echo "======================================"
    echo "Generated: $(date)"
    echo "System: $(uname -s) $(uname -m)"
    echo "User: $(whoami)"
    echo ""
} > "$REPORT_FILE"

# Color output functions
pass() {
    echo "✓ $1"
    echo "✓ $1" >> "$REPORT_FILE"
}

fail() {
    echo "✗ $1"
    echo "✗ $1" >> "$REPORT_FILE"
}

warn() {
    echo "⚠ $1"
    echo "⚠ $1" >> "$REPORT_FILE"
}

info() {
    echo "ℹ $1"
    echo "ℹ $1" >> "$REPORT_FILE"
}

# ============================================================================
# 1. DIRECTORY STRUCTURE
# ============================================================================
echo ""
echo "1. DIRECTORY STRUCTURE"
echo "======================"
{
    echo ""
    echo "1. Directory Structure"
    echo "====================="
} >> "$REPORT_FILE"

if [ -d "$AVATARIFY_DIR" ]; then
    pass "Avatarify directory exists: $AVATARIFY_DIR"
else
    fail "Avatarify directory not found: $AVATARIFY_DIR"
    exit 1
fi

if [ -d "$VENV_PATH" ]; then
    pass "Virtual environment exists: $VENV_PATH"
else
    fail "Virtual environment not found: $VENV_PATH"
fi

# Check required files
for file in "run.py" "run.sh"; do
    if [ -f "$AVATARIFY_DIR/$file" ]; then
        pass "$file exists"
    else
        warn "$file not found"
    fi
done

# Check shell scripts
for script in "setup_avatarify_aws.sh" "start_avatarify_aws.sh"; do
    if [ -f "$AVATARIFY_DIR/$script" ]; then
        pass "$script exists"
        if [ -x "$AVATARIFY_DIR/$script" ]; then
            pass "$script is executable"
        else
            warn "$script exists but not executable (needs: chmod +x $script)"
        fi
    else
        fail "$script not found"
    fi
done

# ============================================================================
# 2. PYTHON ENVIRONMENT
# ============================================================================
echo ""
echo "2. PYTHON ENVIRONMENT"
echo "====================="
{
    echo ""
    echo "2. Python Environment"
    echo "====================="
} >> "$REPORT_FILE"

PYTHON_EXE="$VENV_PATH/bin/python"

if [ ! -f "$PYTHON_EXE" ]; then
    fail "Python executable not found at $PYTHON_EXE"
else
    pass "Python executable found"

    # Get Python version
    PYTHON_VERSION=$($PYTHON_EXE --version 2>&1)
    pass "Python version: $PYTHON_VERSION"
fi

# ============================================================================
# 3. PYTHON PACKAGES
# ============================================================================
echo ""
echo "3. PYTHON PACKAGES"
echo "=================="
{
    echo ""
    echo "3. Python Packages"
    echo "=================="
} >> "$REPORT_FILE"

if [ -f "$PYTHON_EXE" ]; then
    PACKAGES=(
        "cv2:opencv"
        "zmq:pyzmq"
        "msgpack_numpy:msgpack_numpy"
        "yaml:pyyaml"
        "numpy:numpy"
        "pyfakewebcam:pyfakewebcam"
        "requests:requests"
        "scipy:scipy"
        "skimage:scikit-image"
        "PIL:pillow"
    )

    for package_info in "${PACKAGES[@]}"; do
        IFS=':' read -r import_name pkg_name <<< "$package_info"

        if $PYTHON_EXE -c "import $import_name" 2>/dev/null; then
            pass "Package installed: $pkg_name"
        else
            fail "Package missing: $pkg_name (import: $import_name)"
        fi
    done
else
    fail "Cannot check packages - Python not found"
fi

# ============================================================================
# 4. SYSTEM TOOLS
# ============================================================================
echo ""
echo "4. SYSTEM TOOLS"
echo "==============="
{
    echo ""
    echo "4. System Tools"
    echo "==============="
} >> "$REPORT_FILE"

# Check ffmpeg
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -1)
    pass "ffmpeg installed: $FFMPEG_VERSION"
else
    fail "ffmpeg not found - install with: sudo apt install ffmpeg"
fi

# Check ffprobe
if command -v ffprobe &> /dev/null; then
    pass "ffprobe installed"
else
    fail "ffprobe not found - install with: sudo apt install ffmpeg"
fi

# Check bash
if command -v bash &> /dev/null; then
    BASH_VERSION=$(bash --version | head -1)
    pass "bash available: $BASH_VERSION"
else
    fail "bash not found"
fi

# ============================================================================
# 5. VIDEO FILE
# ============================================================================
echo ""
echo "5. VIDEO FILE"
echo "============="
{
    echo ""
    echo "5. Video File"
    echo "============="
} >> "$REPORT_FILE"

if [ -f "$VIDEO_FILE" ]; then
    pass "Video file exists: $VIDEO_FILE"

    SIZE=$(ls -lh "$VIDEO_FILE" | awk '{print $5}')
    pass "File size: $SIZE"

    # Get video properties
    if command -v ffprobe &> /dev/null; then
        VIDEO_INFO=$(ffprobe -v error -select_streams v:0 \
          -show_entries stream=width,height,r_frame_rate,codec_name,duration \
          -of csv=p=0 "$VIDEO_FILE" 2>/dev/null)

        if [ ! -z "$VIDEO_INFO" ]; then
            IFS=',' read -r WIDTH HEIGHT FPS CODEC DURATION <<< "$VIDEO_INFO"
            pass "Video resolution: ${WIDTH}x${HEIGHT}"
            pass "Video codec: $CODEC"
            pass "Frame rate: $FPS"
            pass "Duration: ${DURATION}s"
        else
            warn "Could not read video metadata"
        fi
    fi
else
    warn "Video file not found: $VIDEO_FILE"
    info "Expected at: /home/nathan/Videos/video GEN 01/VIDEO 0001.mp4"
fi

# ============================================================================
# 6. NETWORK CONNECTIVITY
# ============================================================================
echo ""
echo "6. NETWORK CONNECTIVITY"
echo "======================="
{
    echo ""
    echo "6. Network Connectivity"
    echo "======================="
} >> "$REPORT_FILE"

# Check internet
if ping -c 1 -W 2 8.8.8.8 &> /dev/null; then
    pass "Internet connectivity: OK"
else
    warn "Internet connectivity: FAILED (may not be critical)"
fi

# Check if we can reach AWS (if instance IP provided)
AWS_HOST="13.210.132.155"
AWS_PORT=5557

if timeout 2 bash -c "cat < /dev/null > /dev/tcp/$AWS_HOST/$AWS_PORT" 2>/dev/null; then
    pass "AWS proxy reachable: $AWS_HOST:$AWS_PORT"
else
    warn "AWS proxy not reachable: $AWS_HOST:$AWS_PORT (may not be running yet)"
fi

# ============================================================================
# 7. SYSTEM RESOURCES
# ============================================================================
echo ""
echo "7. SYSTEM RESOURCES"
echo "==================="
{
    echo ""
    echo "7. System Resources"
    echo "==================="
} >> "$REPORT_FILE"

# Memory
MEM_INFO=$(free -h | grep "^Mem:")
pass "Memory: $MEM_INFO"

# Disk space
DISK_INFO=$(df -h / | tail -1)
pass "Disk: $DISK_INFO"

# CPU
CPU_COUNT=$(nproc)
pass "CPU cores: $CPU_COUNT"

# ============================================================================
# 8. EXECUTABLE SCRIPTS TEST
# ============================================================================
echo ""
echo "8. SCRIPT EXECUTION TEST"
echo "========================"
{
    echo ""
    echo "8. Script Execution Test"
    echo "========================"
} >> "$REPORT_FILE"

# Test setup script syntax
if [ -f "$AVATARIFY_DIR/setup_avatarify_aws.sh" ]; then
    if bash -n "$AVATARIFY_DIR/setup_avatarify_aws.sh" 2>/dev/null; then
        pass "setup_avatarify_aws.sh: Syntax OK"
    else
        fail "setup_avatarify_aws.sh: Syntax error"
    fi
fi

# Test start script syntax
if [ -f "$AVATARIFY_DIR/start_avatarify_aws.sh" ]; then
    if bash -n "$AVATARIFY_DIR/start_avatarify_aws.sh" 2>/dev/null; then
        pass "start_avatarify_aws.sh: Syntax OK"
    else
        fail "start_avatarify_aws.sh: Syntax error"
    fi
fi

# ============================================================================
# 9. QUICK FUNCTIONALITY TEST
# ============================================================================
echo ""
echo "9. QUICK FUNCTIONALITY TEST"
echo "==========================="
{
    echo ""
    echo "9. Quick Functionality Test"
    echo "==========================="
} >> "$REPORT_FILE"

# Test Python venv activation
if [ -f "$VENV_PATH/bin/activate" ]; then
    if source "$VENV_PATH/bin/activate" 2>/dev/null; then
        pass "Virtual environment activation: OK"

        # Quick import test
        if python3 -c "import numpy; print('numpy version:', numpy.__version__)" 2>/dev/null; then
            NUMPY_VERSION=$(python3 -c "import numpy; print(numpy.__version__)")
            pass "numpy import test: OK (version $NUMPY_VERSION)"
        fi

        deactivate 2>/dev/null || true
    else
        fail "Virtual environment activation failed"
    fi
else
    fail "Virtual environment activation script not found"
fi

# ============================================================================
# SUMMARY
# ============================================================================
echo ""
echo "=============================================="
echo "VALIDATION COMPLETE"
echo "=============================================="
echo ""
echo "Full report saved to: $REPORT_FILE"
echo ""

# Count results
PASSES=$(grep "^✓" "$REPORT_FILE" | wc -l)
FAILS=$(grep "^✗" "$REPORT_FILE" | wc -l)
WARNS=$(grep "^⚠" "$REPORT_FILE" | wc -l)

echo "Summary:"
echo "  ✓ Passed: $PASSES"
echo "  ✗ Failed: $FAILS"
echo "  ⚠ Warnings: $WARNS"
echo ""

if [ $FAILS -eq 0 ]; then
    echo "✓ All critical checks passed!"
    echo ""
    echo "Ready to use:"
    echo "  1. Start Colab worker"
    echo "  2. Run: ~/Downloads/avatarify-python-master/start_avatarify_aws.sh \\"
    echo "       \"/home/nathan/Videos/video GEN 01/VIDEO 0001.mp4\""
    echo "  3. Monitor in Colab"
    exit 0
else
    echo "✗ Please fix the above issues before proceeding"
    exit 1
fi
