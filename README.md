# Timecode Calculator

## What is this?

Working with video timecodes in Excel is frustrating because Excel doesn't understand the `hh:mm:ss:ff` format (hours:minutes:seconds:frames). When you try to add up timecodes like `00:01:30:15 + 00:02:45:10`, Excel treats them as regular numbers instead of timecodes, giving you wrong results.

**This tool solves that problem.** It's a simple calculator specifically designed for video timecodes. You can paste a list of timecodes from Excel, set your framerate (24fps, 25fps, 30fps, etc.), and get the correct sum instantly. Then copy the result right back into Excel.

Perfect for video editors, producers, and anyone working with timecodes who needs quick, accurate calculations.

## Features

- Add multiple timecodes together with proper frame handling
- Support for various framerates (23.976, 24, 25, 29.97, 30, 50, 60 fps)
- Simple web interface - no command line knowledge needed
- Copy/paste directly from Excel
- One-click copy of results back to Excel

---

## Installation and Use

### First Time Setup (One-Time Only)

**Step 1: Install uv (Required)**

`uv` is a tool that helps manage the Python code for this application. You only need to install it once.

**On Windows:**
1. Go to https://docs.astral.sh/uv/getting-started/installation/
2. Download the Windows installer
3. Run the installer and follow the prompts

**On Mac:**
1. Open Terminal (press Cmd+Space, type "Terminal", press Enter)
2. Copy and paste this command, then press Enter:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Follow any prompts that appear

**On Linux:**
1. Open your terminal
2. Copy and paste this command, then press Enter:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Follow any prompts that appear

**Step 2: Download this project**

Download or clone this repository to your computer and unzip it if needed.

---

### Running the Application

**Every time you want to use the calculator:**

1. **Find the launcher file for your system:**
   - Windows: Double-click `start.bat`
   - Mac: Double-click `start.sh`
   - Linux: Double-click `start.sh` (or open terminal, navigate to the folder, and run `./start.sh`)

2. **Wait a few seconds** - The first time you run it, the launcher will automatically:
   - Download and install required components
   - Start the web server
   - Open your web browser to the calculator

3. **Use the calculator:**
   - Select your project's framerate from the dropdown menu
   - Paste your timecodes from Excel (one per line)
   - Click "Calculate Sum"
   - Click "Copy to Clipboard" to copy the result back to Excel

4. **To stop the application:**
   - Close the terminal/command window that opened
   - Or press `Ctrl+C` in the terminal window

---

### Using the Calculator

**Example:**

If you have these timecodes in Excel:
```
00:01:15:10
00:02:30:05
00:00:45:12
```

1. Copy them from Excel
2. Paste into the calculator
3. Select your framerate (e.g., 25 fps)
4. Click "Calculate Sum"
5. Result: `00:04:31:02`
6. Click "Copy to Clipboard" and paste back into Excel

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
