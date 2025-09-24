@echo off
REM Kaspa Docker Setup Wizard for Windows
REM Developed by KaspaDev (KRCBOT)

title Kaspa Docker Setup Wizard

echo.
echo ======================================================================
echo         🚀 Kaspa Docker Setup Wizard 🚀
echo         Developed by KaspaDev (KRCBOT)
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
if not exist "docker-compose.yml" (
    echo ❌ Error: docker-compose.yml not found!
    echo.
    echo Please run this wizard from the Kaspa Docker directory.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found - Starting setup wizard...
echo.

REM Run the Python wizard
python setup-wizard.py

REM Check if wizard completed successfully
if %errorlevel% equ 0 (
    echo.
    echo ✅ Setup wizard completed successfully!
) else (
    echo.
    echo ❌ Setup wizard encountered an error.
)

echo.
pause
