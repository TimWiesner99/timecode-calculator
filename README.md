# Timecode Calculator

A web-based tool for performing calculations with timecodes in `hh:mm:ss:ff` format (hours:minutes:seconds:frames).

## Features

- Add multiple timecodes together
- Support for various framerates (23.976, 24, 25, 29.97, 30, 50, 60 fps)
- Simple web interface for easy copy/paste from Excel
- Copy results back to clipboard for Excel

## Quick Start (Easiest Method)

**For non-technical users**, simply double-click the launcher for your platform:

- **Windows**: Double-click `start.bat`
- **Mac/Linux**: Double-click `start.sh` (or run `./start.sh` in terminal)
- **All platforms**: Run `python start.py`

The launcher will:
1. Check if `uv` is installed (and guide you to install it if needed)
2. Install/update dependencies automatically
3. Start the application
4. Open your browser automatically to http://localhost:5000

## Manual Installation

If you prefer to set up manually:

1. Clone the repository:
```bash
git clone <repository-url>
cd timecode-calculator
```

2. Install dependencies:
```bash
uv sync
```

## Manual Usage

1. Start the Flask application:
```bash
uv run python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Select your framerate from the dropdown
4. Paste your timecodes (one per line) into the text area
5. Click "Calculate Sum"
6. Copy the result back to Excel using the "Copy to Clipboard" button

## Prerequisites

You need to install `uv` (a fast Python package manager):

- **Windows**: Download from https://docs.astral.sh/uv/getting-started/installation/
- **Mac/Linux**: Run `curl -LsSf https://astral.sh/uv/install.sh | sh`

The launcher scripts will check for this and guide you if it's missing.

## Timecode Format

Timecodes must be in the format `hh:mm:ss:ff`:
- `hh`: hours (00-99)
- `mm`: minutes (00-59)
- `ss`: seconds (00-59)
- `ff`: frames (00 to framerate-1)

### Examples
- `00:00:10:00` - 10 seconds
- `00:01:30:12` - 1 minute, 30 seconds, 12 frames
- `01:15:45:23` - 1 hour, 15 minutes, 45 seconds, 23 frames

## Project Structure

```
timecode-calculator/
├── app.py              # Flask web application
├── timecode.py         # Timecode calculation logic
├── start.bat           # Windows launcher
├── start.sh            # Mac/Linux launcher
├── start.py            # Cross-platform Python launcher
├── pyproject.toml      # Python project configuration
├── uv.lock             # Dependency lock file
├── requirements.txt    # Python dependencies (legacy)
├── templates/
│   └── index.html     # Web interface
└── static/
    ├── style.css      # Styling
    └── script.js      # Frontend logic
```

## Future Enhancements

- Subtraction of timecodes
- Multiplication/division operations
- Conversion between different framerates
- Batch processing of multiple calculations
