#!/usr/bin/env python3
"""
Cross-platform launcher for Timecode Calculator.
Works on Windows, Mac, and Linux.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path


def print_header():
    """Print the application header."""
    print("=" * 40)
    print("Timecode Calculator")
    print("=" * 40)
    print()


def check_uv():
    """Check if uv is installed."""
    try:
        subprocess.run(
            ["uv", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_dependencies():
    """Install dependencies using uv sync."""
    print("Installing/updating dependencies...")
    try:
        result = subprocess.run(
            ["uv", "sync"],
            cwd=Path(__file__).parent,
            check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def open_browser():
    """Open the browser to the application URL."""
    time.sleep(2)  # Wait for server to start
    try:
        webbrowser.open("http://localhost:5000")
    except Exception:
        pass  # Silently fail if browser can't be opened


def run_app():
    """Run the Flask application."""
    print()
    print("Starting Timecode Calculator...")
    print()
    print("The application will open in your browser at:")
    print("http://localhost:5000")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    print()

    # Open browser in a separate thread
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Run the Flask app
    try:
        subprocess.run(
            ["uv", "run", "python", "app.py"],
            cwd=Path(__file__).parent,
            check=True
        )
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\n\nERROR: Failed to start application: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    print_header()

    # Check if uv is installed
    if not check_uv():
        print("ERROR: uv is not installed!")
        print()
        print("Please install uv first:")
        print("  Windows: https://docs.astral.sh/uv/getting-started/installation/")
        print("  Mac/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print()
        input("Press Enter to exit...")
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        print()
        print("ERROR: Failed to install dependencies")
        input("Press Enter to exit...")
        sys.exit(1)

    # Run the application
    run_app()


if __name__ == "__main__":
    main()
