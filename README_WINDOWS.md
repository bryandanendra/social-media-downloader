# Windows Installation Guide

Complete guide on how to install and use the Video Downloader application on Windows. Follow the steps in the correct order!

## Quick Usage Guide

1. Open the application by double-clicking on the EXE file or desktop shortcut
2. Paste the video URL from YouTube/Instagram/TikTok
3. Click the download button
4. Wait until the process completes
5. The file will be saved in the "downloads" folder

## Requirements

- [Python 3.x](https://www.python.org/downloads/) (Make sure it's version 3.8 or newer)
- [XAMPP](https://www.apachefriends.org/download.html) (Webserver)
- [FFmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/latest) (Required for video conversion)
- Git (optional, only if you want to use clone)

## Installation Steps (For Beginners)

### 1. Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. **IMPORTANT!** During installation, check the "Add Python to PATH" box
   ![Add Python to PATH](https://python-docs.readthedocs.io/en/latest/_images/win_installer.png)
3. Click "Install Now"
4. Wait until the installation process completes

### 2. Install XAMPP

1. Download XAMPP from [apachefriends.org](https://www.apachefriends.org/download.html)
2. Run the installer and follow the instructions
3. Install in the default location (`C:\xampp`)

### 3. Install FFmpeg (Important!)

1. Download FFmpeg from [GitHub releases](https://github.com/BtbN/FFmpeg-Builds/releases/latest)
   - Choose the `ffmpeg-master-latest-win64-gpl.zip` file
2. Extract the ZIP file to a permanent location, such as `C:\FFmpeg`
3. Add FFmpeg to the Windows PATH:
   - Press `Win + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - In the "System Variables" section, find "Path", select it and click "Edit"
   - Click "New" and add the path to the FFmpeg bin folder (example: `C:\FFmpeg\bin`)
   - Click "OK" on all dialog windows
4. Restart Command Prompt/PowerShell if already open

> **Important Note**: Without FFmpeg, the application cannot download YouTube videos in MP3 format or merge video/audio formats.

### 4. Download the Application

**Method 1: Using Git** (for those already familiar)
1. Open Command Prompt or PowerShell
2. Type the following command:
   ```
   cd C:\xampp\htdocs
   git clone https://github.com/bryandanendra/social-media-downloader.git
   ```

**Method 2: Download ZIP** (easier for beginners)
1. Visit [https://github.com/bryandanendra/social-media-downloader](https://github.com/bryandanendra/social-media-downloader)
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to the `C:\xampp\htdocs\social-media-downloader` folder

### 5. Set Up the Application

1. Open Command Prompt as Administrator
   - Press the Windows key
   - Type "cmd"
   - Right-click on "Command Prompt" and select "Run as administrator"

2. Navigate to the application folder:
   ```
   cd C:\xampp\htdocs\social-media-downloader
   ```

3. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   > If the python command is not recognized, try using `py` instead

4. Install all requirements:
   ```
   pip install -r requirements.txt
   ```
   > This process might take a few minutes, please be patient

## Running the Application

### Easy Method (Development Mode)

1. Make sure you are in the application folder and the virtual environment is active:
   ```
   cd C:\xampp\htdocs\social-media-downloader
   venv\Scripts\activate
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Open a browser and access:
   ```
   http://127.0.0.1:8000
   ```

### Create a Desktop Application

If you want to create an application that can be opened directly without Command Prompt:

1. Make sure the virtual environment is active:
   ```
   cd C:\xampp\htdocs\social-media-downloader
   venv\Scripts\activate
   ```

2. Install PyInstaller if not already installed:
   ```
   pip install pyinstaller
   ```

3. Build the application:
   ```
   pyinstaller app.spec
   ```
   > This process might take 5-10 minutes

4. Copy the build result:
   ```
   xcopy /E /I /Y "dist\YT Downloader" "C:\Program Files\YT Downloader"
   ```

5. Create a desktop shortcut:
   - Open File Explorer
   - Open the `C:\Program Files\YT Downloader` folder
   - Right-click on the `YT Downloader.exe` file
   - Select "Create shortcut"
   - Drag the shortcut to the Desktop

## Application Features

- ✨ Modern and easy-to-use interface
- 🎥 Download videos from:
  - YouTube (MP4 and MP3 formats)
  - Instagram (Reels and Posts)
  - TikTok (Videos)
- 🔍 Automatic platform detection
- 📁 Quick access to the download folder
- 🖼️ Image converter from HEIC to JPG/PNG

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

### Can't access the downloads folder
- Run the application as Administrator
- Check folder permissions

### Error "ffmpeg is not installed" or "You have requested merging of multiple formats but ffmpeg is not installed"
- Make sure FFmpeg is properly installed (see the "Install FFmpeg" section above)
- Verify FFmpeg is registered in PATH by running `ffmpeg -version` in Command Prompt
- If still problematic, try reinstalling FFmpeg in a different location (e.g., `C:\Program Files\FFmpeg`)
- Make sure the FFmpeg bin folder (containing ffmpeg.exe) is added to the system PATH
- Restart your computer after adding FFmpeg to PATH

## Help & Support

If you experience issues, please:
1. Open an issue in the repository: https://github.com/bryandanendra/social-media-downloader/issues
2. Contact @bryandanendra
3. Run the application through Command Prompt to see detailed errors 