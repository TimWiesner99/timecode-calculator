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
echo ""
echo "The application will open in your browser at:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"
echo ""

# Open browser (works on macOS and most Linux systems)
sleep 2
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:5000 2>/dev/null &
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:5000 2>/dev/null &
    fi
fi

# Run the Flask app
uv run python app.py
