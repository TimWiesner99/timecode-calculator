# Timecode Calculator

A web-based tool for performing calculations with timecodes in `hh:mm:ss:ff` format (hours:minutes:seconds:frames).

## Features

- Add multiple timecodes together
- Support for various framerates (23.976, 24, 25, 29.97, 30, 50, 60 fps)
- Simple web interface for easy copy/paste from Excel
- Copy results back to clipboard for Excel

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd timecode-calculator
```

2. Install dependencies:
```bash
uv sync
```

## Usage

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
├── requirements.txt    # Python dependencies
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
