# Video Downloader and Photo Converter.

A simple web application to download videos from YouTube, Instagram, and TikTok. Built with Python Flask and a modern web interface using Tailwind CSS.

## Feature

- ✨ Modern and responsive user interface
- 🎥 Supports downloads from:
  - YouTube (MP4 and MP3 formats)
  - Instagram (Reels and Posts)
  - TikTok (Videos)
- 🔍 Automatic platform detection from pasted URLs
- 📁 Quick button to open download folder
- 🎯 Automatic file title cleaning
- 🔒 Runs locally for security (no internet needed to run the application)
- 🖼️ Integrated image converter (including HEIC support for iPhone)

## UI Preview

![App UI Preview](UI.png)

## Quick Usage Guide

1. Open the application in your browser (http://127.0.0.1:8000)
2. Paste the video URL you want to download
3. The platform will be detected automatically
4. Click the download button
5. Wait for the download process to complete
6. The file will be saved in the "downloads" folder.

## System Requirements

For **macOS & Linux** users:
- Python 3.x
- XAMPP or other web server

**Note**: For Windows users, please see [README_WINDOWS.md](README_WINDOWS.md)

## Installation (macOS & Linux)

1. Download or clone this repository:
```bash
git clone https://github.com/bryandanendra/social-media-downloader.git
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
```

3. Install all requirements:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and access the following address:
```
http://127.0.0.1:8060
```

## Managing Dependencies

### Updating Dependencies

To keep your dependencies up to date, use the `update_dependencies.sh` script:

```bash
bash update_dependencies.sh
```

**What this script does:**
- 🔄 Updates pip to the latest version
- 📦 Updates all packages to their latest versions
- ✅ Checks current and updated versions
- 🚀 Ensures compatibility with the latest features

**Supported packages:**
- Flask (Web framework)
- yt-dlp (Video downloader)
- Pillow (Image processing)
- pillow-heif (HEIC support)
- pdf2image (PDF conversion)
- pathlib (File utilities)

### Development Dependencies

For development work, additional dependencies are available:

```bash
pip install -r requirements-dev.txt
```

**Development tools included:**
- pytest (Testing framework)
- black (Code formatting)
- flake8 (Code linting)
- mypy (Type checking)
- pre-commit (Git hooks)
- sphinx (Documentation)

## Creating a Desktop Application (Optional)

### Method 1: Using create_simple_app.sh (Recommended for macOS)

This script creates a native macOS `.app` bundle that can be double-clicked to run:

1. Make sure you are in the project directory:
```bash
cd /Users/a1234/Documents/CODING/Donverter
```

2. Run the script to create the app bundle:
```bash
bash create_simple_app.sh
```

3. The script will create `Donverter.app` in your project directory

4. Double-click `Donverter.app` in Finder to run the application

**Features of the macOS App Bundle:**
- 🍎 Native macOS application
- 📱 One-click launch from Finder
- 🌐 Automatically opens browser to `http://127.0.0.1:8060`
- 💻 Terminal window shows application logs
- 🚀 Can be dragged to Dock for quick access

### Method 2: Using PyInstaller (Alternative)

If you want to create an application that can be opened directly without a terminal, follow these steps:

1. Make sure you are in the project directory and the virtual environment is active:
```bash
cd /Applications/XAMPP/xamppfiles/htdocs/social-media-downloader
source venv/bin/activate
```

2. Build the application with PyInstaller:
```bash
pyinstaller app.spec
```

3. Move the build to Applications:
```bash
cp -R "dist/YT Downloader" "/Applications/YT Downloader"
```

4. Run the application from the Applications folder

## Using the Image Converter

This application also has a feature to convert image formats:
1. Click the "Image Converter" menu in the application
2. Upload an image (including HEIC format from iPhone)
3. Select the output format (JPG, PNG, or PDF)
4. Click 'Convert' to change the image format
5. Download the conversion result

### Supported Formats:
- **Input**: HEIC (iPhone), JPG, JPEG, PNG
- **Output**: JPG, PNG, PDF

This conversion feature is especially useful for iPhone users who want to convert HEIC photos to more commonly used formats like JPG, PNG, or PDF.

## Folder Structure

```
social-media-downloader/
├── cache/                    # Cache for frequently accessed URLs
├── downloads/                # Folder for downloaded files
├── uploads/                  # Folder for uploaded files (image converter)
├── converted/                # Folder for converted images
├── templates/                # HTML templates
├── venv/                     # Python virtual environment
├── app.py                    # Flask server application
├── run_app.py                # Script to run the desktop application
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── create_simple_app.sh      # macOS app bundle creator
├── update_dependencies.sh    # Dependency updater
├── Donverter.app/            # macOS application bundle (created by script)
└── app.spec                  # PyInstaller configuration
```

## Script Management

### Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `create_simple_app.sh` | Creates macOS app bundle | `bash create_simple_app.sh` |
| `update_dependencies.sh` | Updates all dependencies | `bash update_dependencies.sh` |
| `app.py` | Main Flask application | `python app.py` |

### Quick Commands

**Start the application:**
```bash
python app.py
```

**Create macOS app:**
```bash
bash create_simple_app.sh
```

**Update dependencies:**
```bash
bash update_dependencies.sh
```

**Access the application:**
- Web interface: `http://127.0.0.1:8060`
- macOS app: Double-click `Donverter.app`

## Important Notes

- This application runs locally (localhost) for security
- **Default port**: 8060 (not 8000 as mentioned in some older documentation)
- Make sure port 8060 is not used by another application
- Use a virtual environment to isolate dependencies
- The downloads, uploads, and converted folders will be created automatically
- macOS app bundle (`Donverter.app`) automatically handles port conflicts

## Help & Support

If you experience issues, please:
1. Open an issue in the repository: https://github.com/bryandanendra/social-media-downloader/issues
2. Contact @bryandanendra
3. Run the application through the terminal to see error messages

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Check what's using port 8060
lsof -i :8060

# Kill the process if needed
lsof -ti :8060 | xargs kill -9
```

**macOS app bundle not working:**
```bash
# Recreate the app bundle
bash create_simple_app.sh

# Check permissions
chmod +x create_simple_app.sh
```

**Dependencies outdated:**
```bash
# Update all dependencies
bash update_dependencies.sh

# Or manually update specific packages
pip install --upgrade flask yt-dlp pillow
```

**Virtual environment issues:**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Getting Help

1. **Check the logs**: Run `python app.py` in terminal to see detailed error messages
2. **Verify dependencies**: Run `bash update_dependencies.sh` to ensure all packages are up to date
3. **Recreate app bundle**: If the macOS app isn't working, run `bash create_simple_app.sh`
4. **Check port**: Ensure port 8060 is available before starting the application

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created by @bryandanendra 