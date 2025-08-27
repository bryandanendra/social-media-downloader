# Windows Installation Guide for Donverter

Complete guide on how to install and use the Donverter application (Video Downloader + Image Converter) on Windows. This application is built with Python Flask and provides a modern web interface.

## Quick Usage Guide

1. **Start the application** by running `python app.py` or using the built executable
2. **Open your browser** and go to `http://127.0.0.1:8060`
3. **Paste the video URL** from YouTube/Instagram/TikTok
4. **Click the download button** and wait for completion
5. **Access the Image Converter** from the menu to convert HEIC/JPEG/PNG files
6. **Files are saved** in the "downloads" and "converted" folders

## Features

- ✨ **Modern web interface** with responsive design
- 🎥 **Video Downloader** supporting YouTube, Instagram, and TikTok
- 🖼️ **Image Converter** with HEIC support (iPhone photos)
- 📄 **PDF to Image conversion** (first page only)
- 🔍 **Automatic platform detection** from URLs
- 📁 **Quick folder access** buttons
- 🚀 **Local web application** (no internet needed to run)

## System Requirements

- **Windows 10/11** (64-bit recommended)
- **Python 3.8 or newer** (Python 3.11+ recommended)
- **4GB RAM** minimum (8GB recommended)
- **500MB free disk space**
- **Internet connection** for downloading videos and installing packages

## Installation Steps (For Beginners)

### 1. Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT!** During installation, check the "Add Python to PATH" box
   ![Add Python to PATH](https://python-docs.readthedocs.io/en/latest/_images/win_installer.png)
3. Click "Install Now"
4. Wait until the installation process completes

### 2. Install Git (Optional but Recommended)

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer with default settings
3. This allows you to clone the repository easily

### 3. Install Poppler (Required for PDF conversion)

**Note**: This is only needed if you want to use the PDF to Image conversion feature.

1. Download Poppler for Windows from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract to a permanent location (e.g., `C:\poppler`)
3. Add to PATH:
   - Press `Win + X` → "System" → "Advanced system settings"
   - Click "Environment Variables"
   - In "System Variables", find "Path" → "Edit"
   - Click "New" and add `C:\poppler\Library\bin`
   - Click "OK" on all dialogs
4. Restart Command Prompt/PowerShell

> **Important Note**: Poppler is required for PDF processing. Without it, PDF conversion features won't work.

### 4. Download the Application

**Method 1: Using Git** (recommended)
1. Open Command Prompt or PowerShell
2. Navigate to your desired directory:
   ```
   cd C:\Users\%USERNAME%\Documents
   ```
3. Clone the repository:
   ```
   git clone https://github.com/bryandanendra/social-media-downloader.git
   cd social-media-downloader
   ```

**Method 2: Download ZIP** (easier for beginners)
1. Visit [https://github.com/bryandanendra/social-media-downloader](https://github.com/bryandanendra/social-media-downloader)
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to a folder (e.g., `C:\Users\%USERNAME%\Documents\social-media-downloader`)
5. Open Command Prompt in that folder

### 5. Set Up the Application

1. **Open Command Prompt as Administrator**:
   - Press `Win + R`, type `cmd`, press `Ctrl + Shift + Enter`
   - Or search "cmd" in Start menu, right-click → "Run as administrator"

2. **Navigate to the application folder**:
   ```cmd
   cd C:\Users\%USERNAME%\Documents\social-media-downloader
   ```

3. **Create and activate a Python virtual environment**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
   > If `python` is not recognized, try using `py` instead

4. **Install all requirements**:
   ```cmd
   pip install -r requirements.txt
   ```
   > This process might take a few minutes, please be patient

## Running the Application

### Method 1: Direct Python Execution (Recommended for Development)

1. **Make sure you are in the application folder and the virtual environment is active**:
   ```cmd
   cd C:\Users\%USERNAME%\Documents\social-media-downloader
   venv\Scripts\activate
   ```

2. **Run the application**:
   ```cmd
   python app.py
   ```

3. **Open your browser and access**:
   ```
   http://127.0.0.1:8060
   ```

### Method 2: Using run_app.py (Alternative)

1. **With virtual environment active**:
   ```cmd
   python run_app.py
   ```

2. **This will open the browser automatically to**:
   ```
   http://127.0.0.1:5000
   ```

### Method 3: Create a Desktop Application (Advanced)

If you want to create an executable that can be opened directly:

1. **Install PyInstaller**:
   ```cmd
   pip install pyinstaller
   ```

2. **Build the application**:
   ```cmd
   pyinstaller app.spec
   ```
   > This process might take 5-10 minutes

3. **Find the executable** in the `dist\YT Downloader` folder

4. **Create a desktop shortcut**:
   - Right-click on `YT Downloader.exe`
   - Select "Create shortcut"
   - Drag the shortcut to the Desktop

## Application Features

- ✨ **Modern web interface** with responsive design
- 🎥 **Video Downloader** supporting:
  - YouTube (MP4 and MP3 formats)
  - Instagram (Reels and Posts)
  - TikTok (Videos)
- 🖼️ **Image Converter** supporting:
  - HEIC (iPhone photos) → JPG/PNG
  - JPG/JPEG → PNG/PDF
  - PNG → JPG/PDF
  - PDF → PNG/JPG (first page only)
- 🔍 **Automatic platform detection** from URLs
- 📁 **Quick folder access** buttons
- 🚀 **Local web application** (no internet needed to run)
- 💾 **File caching** for faster repeated downloads

## Troubleshooting Common Issues

### "Python not found" or "Python is not recognized"
- Make sure Python is installed
- Make sure you checked "Add Python to PATH" during installation
- Restart your computer after installing Python
- Try using the `py` command instead of `python`

### Error when installing packages
- Make sure Command Prompt is run as Administrator
- Make sure your internet connection is stable
- Update pip first: `pip install --upgrade pip`
- If there's an error with a specific package, try installing them one by one

### Application won't open or crashes
- Make sure antivirus is not blocking the application
- Run the application as Administrator
- Check Windows Event Viewer for error details

### Port already in use errors
- The application uses port 8060 by default
- Check if port is in use: `netstat -an | findstr 8060`
- Kill conflicting processes or use a different port

### PDF conversion not working
- Make sure Poppler is properly installed and added to PATH
- Verify installation: `pdftoppm -help` in Command Prompt
- Restart Command Prompt after adding Poppler to PATH

### HEIC images not converting
- Make sure `pillow-heif` is installed: `pip install pillow-heif`
- Check if the package is in requirements.txt

### Can't access the downloads/converted folders
- Run the application as Administrator
- Check folder permissions
- Make sure the folders exist in the application directory

## Windows-Specific Scripts and Management

### Creating Windows Batch Files

You can create convenient batch files for Windows:

**Create `start_donverter.bat`:**
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python app.py
pause
```

**Create `update_deps.bat`:**
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
pause
```

### PowerShell Scripts

**Create `start_donverter.ps1`:**
```powershell
Set-Location $PSScriptRoot
.\venv\Scripts\Activate.ps1
python app.py
```

**Note**: You may need to change PowerShell execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows Service (Advanced)

For production use, you can create a Windows service using tools like:
- NSSM (Non-Sucking Service Manager)
- WinSW (Windows Service Wrapper)
- Python Windows Service

## Help & Support

If you experience issues, please:
1. Open an issue in the repository: https://github.com/bryandanendra/social-media-downloader/issues
2. Contact @bryandanendra
3. Run the application through Command Prompt to see detailed errors
4. Check the troubleshooting section above for common solutions 