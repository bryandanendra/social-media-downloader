#!/bin/bash

# Update Dependencies Script for Donverter
# Script ini akan mengupdate semua dependencies ke versi terbaru

echo "🔄 Update Dependencies Donverter"
echo "================================"
echo ""

# Dapatkan path direktori script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Aktifkan virtual environment
echo "🔧 Mengaktifkan virtual environment..."
source venv/bin/activate

echo "✅ Virtual environment aktif"
echo "🐍 Python path: $(which python)"
echo ""

# Cek versi saat ini
echo "📋 Versi dependencies saat ini:"
echo "--------------------------------"
python -c "
import flask, yt_dlp, PIL, pillow_heif, pdf2image
print(f'Flask: {flask.__version__}')
print(f'yt-dlp: {yt_dlp.version.__version__}')
print(f'Pillow: {PIL.__version__}')
print(f'pillow-heif: {pillow_heif.__version__}')
print(f'pdf2image: {pdf2image.__version__}')
" 2>/dev/null || echo "❌ Ada package yang belum terinstall"
echo ""

# Update pip
echo "🔄 Update pip..."
pip install --upgrade pip

# Update semua dependencies
echo ""
echo "📦 Update dependencies ke versi terbaru..."
pip install --upgrade flask yt-dlp pillow pillow-heif pdf2image pathlib

# Install dependencies dari requirements.txt
echo ""
echo "📋 Install dependencies dari requirements.txt..."
pip install -r requirements.txt

# Cek versi setelah update
echo ""
echo "📋 Versi dependencies setelah update:"
echo "-------------------------------------"
python -c "
import flask, yt_dlp, PIL, pillow_heif, pdf2image
print(f'Flask: {flask.__version__}')
print(f'yt-dlp: {yt_dlp.version.__version__}')
print(f'Pillow: {PIL.__version__}')
print(f'pillow-heif: {pillow_heif.__version__}')
print(f'pdf2image: {pdf2image.__version__}')
" 2>/dev/null || echo "❌ Ada package yang belum terinstall"

echo ""
echo "🎯 Update selesai!"
echo "💡 Tips:"
echo "   - Gunakan requirements.txt untuk production"
echo "   - Gunakan requirements-dev.txt untuk development"
echo "   - Gunakan requirements-minimal.txt untuk minimal setup"
echo ""
echo "🚀 Donverter siap digunakan dengan dependencies terbaru!"
