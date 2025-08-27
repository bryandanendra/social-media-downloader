@echo off
REM Start Donverter Application for Windows
REM This batch file will start the Donverter application

echo.
echo ========================================
echo           DONVERTER FOR WINDOWS
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if requirements are installed
echo Checking dependencies...
python -c "import flask, yt_dlp, PIL, pillow_heif" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if port 8060 is available
echo Checking port 8060...
netstat -an | findstr ":8060" >nul 2>&1
if not errorlevel 1 (
    echo WARNING: Port 8060 is already in use
    echo Trying to free the port...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8060"') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 >nul
)

REM Start the application
echo.
echo Starting Donverter...
echo Web interface will be available at: http://127.0.0.1:8060
echo.
echo Press Ctrl+C to stop the application
echo.

python app.py

REM If we get here, the application has stopped
echo.
echo Application stopped.
pause
