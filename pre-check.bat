@echo off
REM Kaspa Docker Pre-Check Script for Windows
REM Developed by KaspaDev (KRCBOT)

echo.
echo ============================================================
echo     Kaspa Docker Pre-Check Script
echo     Developed by KaspaDev (KRCBOT)
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.6+ from https://python.org
    pause
    exit /b 1
)

REM Run the Python pre-check script
python pre-check.py

REM Pause to show results
pause
