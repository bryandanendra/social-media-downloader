@echo off
REM Update Dependencies for Donverter on Windows
REM This batch file will update all dependencies to the latest versions

echo.
echo ========================================
echo      UPDATE DEPENDENCIES - WINDOWS
echo ========================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
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

echo.
echo Current Python path: %VIRTUAL_ENV%\Scripts\python.exe
echo.

REM Update pip
echo Updating pip...
python -m pip install --upgrade pip

REM Update all dependencies
echo.
echo Updating dependencies to latest versions...
pip install --upgrade flask yt-dlp pillow pillow-heif pdf2image pathlib

REM Install from requirements.txt
echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM Check versions after update
echo.
echo ========================================
echo Dependencies after update:
echo ========================================
python -c "
try:
    import flask
    print(f'Flask: {flask.__version__}')
except:
    print('Flask: Not installed')

try:
    import yt_dlp
    print(f'yt-dlp: {yt_dlp.version.__version__}')
except:
    print('yt-dlp: Not installed')

try:
    import PIL
    print(f'Pillow: {PIL.__version__}')
except:
    print('Pillow: Not installed')

try:
    import pillow_heif
    print(f'pillow-heif: {pillow_heif.__version__}')
except:
    print('pillow-heif: Not installed')

try:
    import pdf2image
    print(f'pdf2image: {pdf2image.__version__}')
except:
    print('pdf2image: Not installed')
"

echo.
echo ========================================
echo Update completed!
echo ========================================
echo.
echo Tips:
echo - Use requirements.txt for production
echo - Use requirements-dev.txt for development
echo - Run start_donverter.bat to start the application
echo.
pause
