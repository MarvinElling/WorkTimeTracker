#!/bin/bash
# Work Time Tracker - Unix/Linux/macOS Launcher

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     Work Time Tracker - Unix/Linux/macOS Launcher              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    echo "  Please install Python from https://www.python.org"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Install requirements if needed
echo ""
echo "Checking dependencies..."
pip3 show PyQt5 > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing PyQt5..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "✗ Failed to install dependencies"
        exit 1
    fi
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Run the application
echo ""
echo "Starting Work Time Tracker..."
echo ""
python3 run.py

if [ $? -ne 0 ]; then
    echo "✗ Application failed to start"
    exit 1
fi
