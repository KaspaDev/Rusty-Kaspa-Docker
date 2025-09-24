@echo off
REM Docker & Docker Compose Installation Script for Windows
REM Developed by KaspaDev (KRCBOT)

title Docker Installation Script

echo.
echo ======================================================================
echo     🐳 Docker & Docker Compose Installation Script
echo     Developed by KaspaDev (KRCBOT)
echo ======================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.6+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "install-docker.py" (
    echo ❌ Error: install-docker.py not found!
    echo.
    echo Please run this script from the Kaspa Docker directory.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found - Starting Docker installation...
echo.

REM Run the Python installation script
python install-docker.py

REM Check if installation completed successfully
if %errorlevel% equ 0 (
    echo.
    echo ✅ Docker installation completed successfully!
) else (
    echo.
    echo ❌ Docker installation encountered an error.
)

echo.
pause
