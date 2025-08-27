#!/bin/bash

# Create Simple macOS App Bundle for Donverter
# Script ini akan membuat .app yang bisa dijalankan dengan double-click

echo "🍎 Membuat macOS App Bundle untuk Donverter..."
echo "================================================"

# Dapatkan path direktori script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Nama app
APP_NAME="Donverter.app"
APP_CONTENTS="$APP_NAME/Contents"
APP_MACOS="$APP_CONTENTS/MacOS"
APP_RESOURCES="$APP_CONTENTS/Resources"

echo "📁 Direktori: $SCRIPT_DIR"
echo "📱 Nama App: $APP_NAME"
echo ""

# Hapus app lama jika ada
if [ -d "$APP_NAME" ]; then
    echo "🗑️  Menghapus app lama..."
    rm -rf "$APP_NAME"
fi

# Buat struktur app bundle
echo "📦 Membuat struktur app bundle..."
mkdir -p "$APP_MACOS"
mkdir -p "$APP_RESOURCES"

# Buat Info.plist
echo "📋 Membuat Info.plist..."
cat > "$APP_CONTENTS/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Donverter</string>
    <key>CFBundleIdentifier</key>
    <string>com.donverter.app</string>
    <key>CFBundleName</key>
    <string>Donverter</string>
    <key>CFBundleDisplayName</key>
    <string>Donverter</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
</dict>
</plist>
EOF

# Buat executable script
echo "🔧 Membuat executable script..."
cat > "$APP_MACOS/Donverter" << 'EOF'
#!/bin/bash

# Donverter macOS App Launcher
# Script ini akan dijalankan ketika app dibuka

# Dapatkan path direktori app bundle
APP_BUNDLE="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT_DIR="$(dirname "$APP_BUNDLE")"

# Buka terminal dan jalankan aplikasi
osascript << EOT
tell application "Terminal"
    activate
    do script "cd '$SCRIPT_DIR' && echo '🚀 Memulai Donverter...' && echo '=======================' && echo '' && echo '🔍 Memeriksa sistem...' && echo '' && if ! command -v python3 &> /dev/null; then echo '❌ Python3 tidak ditemukan'; echo '💡 Install Python dengan: brew install python'; echo ''; read -p 'Tekan Enter untuk keluar...'; exit 1; fi && echo '✅ Python3 ditemukan' && echo '' && if [ ! -d 'venv' ]; then echo '📦 Membuat virtual environment...'; python3 -m venv venv; fi && echo '🔧 Mengaktifkan virtual environment...' && source venv/bin/activate && echo '✅ Virtual environment aktif' && echo '' && echo '🔍 Memeriksa dependencies...' && python -c 'import flask, yt_dlp, PIL, pillow_heif, pdf2image' 2>/dev/null || (echo '📦 Menginstall dependencies...' && pip install -r requirements.txt) && echo '✅ Dependencies siap' && echo '' && echo '🔍 Memeriksa port 8000...' && if lsof -i :8000 >/dev/null 2>&1; then echo '⚠️  Port 8000 sudah digunakan'; echo '🔧 Mencoba membebaskan port...'; lsof -ti :8000 | xargs kill -9 2>/dev/null; sleep 2; fi && echo '✅ Port 8000 tersedia' && echo '' && echo '🚀 Memulai Donverter...' && echo '📱 Buka browser: http://127.0.0.1:8000' && echo '⏹️  Tekan Ctrl+C untuk stop' && echo '' && python app.py"
end tell
EOT

# Buka browser otomatis setelah delay
sleep 5
open "http://127.0.0.1:8000"
EOF

# Buat script executable
chmod +x "$APP_MACOS/Donverter"

echo "✅ App bundle berhasil dibuat!"
echo "📱 Lokasi: $SCRIPT_DIR/$APP_NAME"
echo ""
echo "💡 Cara penggunaan:"
echo "   1. Double-click $APP_NAME di Finder"
echo "   2. Terminal akan terbuka otomatis"
echo "   3. Browser akan terbuka ke http://127.0.0.1:8000"
echo "   4. Aplikasi akan berjalan di background"
echo ""
echo "🎯 Tips:"
echo "   - Drag $APP_NAME ke Dock untuk quick access"
echo "   - Bisa dijalankan dari Applications folder"
echo "   - Terminal akan menampilkan log aplikasi"
echo ""
echo "✨ Selesai! Aplikasi macOS Donverter siap digunakan."
