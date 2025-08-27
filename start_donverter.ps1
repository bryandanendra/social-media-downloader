# Start Donverter Application for Windows (PowerShell)
# This PowerShell script will start the Donverter application

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "           DONVERTER FOR WINDOWS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to the directory where this script is located
Set-Location $PSScriptRoot

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Check if requirements are installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import flask, yt_dlp, PIL, pillow_heif" 2>$null
    Write-Host "✅ Dependencies are ready" -ForegroundColor Green
} catch {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check if port 8060 is available
Write-Host "🔍 Checking port 8060..." -ForegroundColor Yellow
$portInUse = Get-NetTCPConnection -LocalPort 8060 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "⚠️  WARNING: Port 8060 is already in use" -ForegroundColor Yellow
    Write-Host "🔧 Trying to free the port..." -ForegroundColor Yellow
    
    $processes = Get-Process -Id $portInUse.OwningProcess -ErrorAction SilentlyContinue
    foreach ($process in $processes) {
        Write-Host "Stopping process: $($process.ProcessName) (PID: $($process.Id))" -ForegroundColor Yellow
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    }
    
    Start-Sleep -Seconds 2
}

# Start the application
Write-Host ""
Write-Host "🚀 Starting Donverter..." -ForegroundColor Green
Write-Host "Web interface will be available at: http://127.0.0.1:8060" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

try {
    python app.py
} catch {
    Write-Host ""
    Write-Host "❌ Application stopped with error" -ForegroundColor Red
}

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
