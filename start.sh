#!/bin/bash
# Timecode Calculator Launcher for Mac/Linux

echo "================================"
echo "Timecode Calculator"
echo "================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv is not installed!"
    echo ""
    echo "Please install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    echo "Or visit: https://docs.astral.sh/uv/getting-started/installation/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Installing/updating dependencies..."
uv sync
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "Starting Timecode Calculator..."
echo "================================"
echo ""

# Run the app
uv run python app.py
