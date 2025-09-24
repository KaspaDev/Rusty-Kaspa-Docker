#!/bin/bash
# Docker & Docker Compose Installation Script for Unix-like systems
# Developed by KaspaDev (KRCBOT)

echo ""
echo "======================================================================"
echo "    🐳 Docker & Docker Compose Installation Script"
echo "    Developed by KaspaDev (KRCBOT)"
echo "======================================================================"
echo ""

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    if python -c "import sys; sys.exit(0 if sys.version_info >= (3, 6) else 1)" 2>/dev/null; then
        PYTHON_CMD="python"
    else
        echo "❌ Python 3.6+ is required but not found"
        echo ""
        echo "Please install Python 3.6+ from your package manager:"
        echo "  • Ubuntu/Debian: sudo apt install python3"
        echo "  • CentOS/RHEL: sudo yum install python3"
        echo "  • macOS: brew install python3"
        echo ""
        exit 1
    fi
else
    echo "❌ Python is not installed or not in PATH"
    echo ""
    echo "Please install Python 3.6+ from your package manager:"
    echo "  • Ubuntu/Debian: sudo apt install python3"
    echo "  • CentOS/RHEL: sudo yum install python3"
    echo "  • macOS: brew install python3"
    echo ""
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "install-docker.py" ]; then
    echo "❌ Error: install-docker.py not found!"
    echo ""
    echo "Please run this script from the Kaspa Docker directory."
    echo ""
    exit 1
fi

echo "✅ Python found - Starting Docker installation..."
echo ""

# Run the Python installation script
$PYTHON_CMD install-docker.py

# Check if installation completed successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Docker installation completed successfully!"
else
    echo ""
    echo "❌ Docker installation encountered an error."
fi

echo ""
