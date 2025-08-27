#!/bin/bash

# Debug YouTube Download Issues
# Script ini akan membantu mendiagnosis masalah download

echo "🔍 Debug YouTube Download Issues"
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

# Cek versi yt-dlp
echo "📦 Cek versi yt-dlp..."
yt_dlp_version=$(python -c "import yt_dlp; print(yt_dlp.version.__version__)" 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "✅ yt-dlp version: $yt_dlp_version"
else
    echo "❌ yt-dlp tidak terinstall"
    exit 1
fi

echo ""

# Test URL yang bermasalah
TEST_URL="https://www.youtube.com/watch?v=NtaGzRXRYrQ&list=RDNtaGzRXRYrQ&start_radio=1"

echo "🧪 Test download dengan URL bermasalah..."
echo "🔗 URL: $TEST_URL"
echo ""

# Test 1: Cek info video
echo "📋 Test 1: Cek info video..."
python -c "
import yt_dlp
ydl_opts = {'quiet': True}
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info('$TEST_URL', download=False)
        print(f'✅ Video title: {info.get(\"title\", \"N/A\")}')
        print(f'✅ Duration: {info.get(\"duration\", \"N/A\")} seconds')
        print(f'✅ Formats available: {len(info.get(\"formats\", []))}')
        
        # Cek format yang tersedia
        formats = info.get('formats', [])
        audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
        video_formats = [f for f in formats if f.get('vcodec') != 'none']
        
        print(f'✅ Audio-only formats: {len(audio_formats)}')
        print(f'✅ Video formats: {len(video_formats)}')
        
        if audio_formats:
            print('🎵 Audio formats available for MP3 conversion')
        else:
            print('⚠️  No audio-only formats available')
            
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""

# Test 2: Coba download MP4
echo "📥 Test 2: Coba download MP4..."
python -c "
import yt_dlp
ydl_opts = {
    'format': 'best[height<=720]',
    'outtmpl': 'test_download_%(title)s.%(ext)s',
    'quiet': False
}
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print('🚀 Starting MP4 download...')
        ydl.download(['$TEST_URL'])
        print('✅ MP4 download successful!')
except Exception as e:
    print(f'❌ MP4 download failed: {e}')
"

echo ""

# Test 3: Coba download MP3
echo "🎵 Test 3: Coba download MP3..."
python -c "
import yt_dlp
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'test_download_%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': False
}
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print('🚀 Starting MP3 download...')
        ydl.download(['$TEST_URL'])
        print('✅ MP3 download successful!')
except Exception as e:
    print(f'❌ MP3 download failed: {e}')
    print('💡 This might be the root cause of your issue')
"

echo ""

# Test 4: Update yt-dlp
echo "🔄 Test 4: Update yt-dlp..."
echo "📦 Updating yt-dlp to latest version..."
pip install --upgrade yt-dlp

echo ""
echo "🎯 Debug selesai!"
echo "💡 Lihat hasil di atas untuk diagnosis masalah"
echo ""
echo "🔧 Solusi yang bisa dicoba:"
echo "1. Update yt-dlp (sudah dilakukan)"
echo "2. Coba download MP4 dulu, lalu convert ke MP3"
echo "3. Gunakan format yang berbeda"
echo "4. Cek apakah video memiliki restriction khusus"
