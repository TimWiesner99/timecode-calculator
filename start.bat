@echo off
REM Timecode Calculator Launcher for Windows

echo ================================
echo Timecode Calculator
echo ================================
echo.

REM Check if uv is installed
where uv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: uv is not installed!
    echo.
    echo Please install uv first:
    echo   https://docs.astral.sh/uv/getting-started/installation/
    echo.
    pause
    exit /b 1
)

echo Installing/updating dependencies...
uv sync
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Starting Timecode Calculator...
echo ================================
echo.

REM Run the app
uv run python app.py

pause
