#!/bin/bash
# Kaspa Docker Pre-Check Script for Unix-like systems
# Developed by KaspaDev (KRCBOT)

echo ""
echo "============================================================"
echo "    Kaspa Docker Pre-Check Script"
echo "    Developed by KaspaDev (KRCBOT)"
echo "============================================================"
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    if python -c "import sys; sys.exit(0 if sys.version_info >= (3, 6) else 1)" 2>/dev/null; then
        PYTHON_CMD="python"
    else
        echo "Python 3.6+ is required but not found"
        echo "Please install Python 3.6+ from your package manager"
        exit 1
    fi
else
    echo "Python is not installed or not in PATH"
    echo "Please install Python 3.6+ from your package manager"
    exit 1
fi

# Run the Python pre-check script
$PYTHON_CMD pre-check.py

# Exit with the same code as the Python script
exit $?
