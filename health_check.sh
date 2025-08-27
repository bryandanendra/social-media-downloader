#!/bin/bash

# Donverter Health Check Script
# Script untuk memeriksa kesehatan aplikasi

echo "🏥 Donverter Health Check"
echo "========================="

# Dapatkan path direktori script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Fungsi untuk check Python
check_python() {
    echo "🐍 Memeriksa Python..."
    
    if command -v python3 &> /dev/null; then
        local python_version=$(python3 --version 2>&1)
        echo "✅ Python ditemukan: $python_version"
        return 0
    elif command -v python &> /dev/null; then
        local python_version=$(python --version 2>&1)
        echo "✅ Python ditemukan: $python_version"
        return 0
    else
        echo "❌ Python tidak ditemukan!"
        echo "💡 Install Python dengan: brew install python"
        return 1
    fi
}

# Fungsi untuk check virtual environment
check_venv() {
    echo "🔧 Memeriksa Virtual Environment..."
    
    if [ -d "venv" ]; then
        echo "✅ Virtual environment ditemukan"
        
        if [ -f "venv/bin/activate" ]; then
            echo "✅ Virtual environment bisa diaktifkan"
            return 0
        else
            echo "⚠️  Virtual environment tidak lengkap"
            return 1
        fi
    else
        echo "⚠️  Virtual environment tidak ditemukan"
        echo "💡 Buat dengan: python3 -m venv venv"
        return 1
    fi
}

# Fungsi untuk check dependencies
check_dependencies() {
    echo "📦 Memeriksa Dependencies..."
    
    if [ -f "requirements.txt" ]; then
        echo "✅ requirements.txt ditemukan"
        
        if [ -d "venv" ]; then
            source venv/bin/activate
            
            # Check key dependencies
            local deps=("flask" "yt_dlp" "PIL" "pillow_heif" "pdf2image")
            local missing_deps=()
            
            for dep in "${deps[@]}"; do
                if python -c "import $dep" 2>/dev/null; then
                    echo "✅ $dep tersedia"
                else
                    echo "❌ $dep tidak tersedia"
                    missing_deps+=("$dep")
                fi
            done
            
            if [ ${#missing_deps[@]} -eq 0 ]; then
                echo "✅ Semua dependencies tersedia"
                return 0
            else
                echo "⚠️  Dependencies yang hilang: ${missing_deps[*]}"
                echo "💡 Install dengan: pip install -r requirements.txt"
                return 1
            fi
        else
            echo "⚠️  Virtual environment tidak aktif"
            return 1
        fi
    else
        echo "❌ requirements.txt tidak ditemukan"
        return 1
    fi
}

# Fungsi untuk check port
check_port() {
    echo "🔌 Memeriksa Port 8000..."
    
    if lsof -i :8000 >/dev/null 2>&1; then
        local process=$(lsof -i :8000 | grep LISTEN | awk '{print $1}')
        echo "⚠️  Port 8000 sudah digunakan oleh: $process"
        return 1
    else
        echo "✅ Port 8000 tersedia"
        return 0
    fi
}

# Fungsi untuk check folder structure
check_folders() {
    echo "📁 Memeriksa Struktur Folder..."
    
    local required_folders=("cache" "downloads" "uploads" "converted" "templates")
    local missing_folders=()
    
    for folder in "${required_folders[@]}"; do
        if [ -d "$folder" ]; then
            echo "✅ $folder/ tersedia"
        else
            echo "❌ $folder/ tidak tersedia"
            missing_folders+=("$folder")
        fi
    done
    
    if [ ${#missing_folders[@]} -eq 0 ]; then
        echo "✅ Semua folder tersedia"
        return 0
    else
        echo "⚠️  Folder yang hilang: ${missing_folders[*]}"
        return 1
    fi
}

# Fungsi untuk check file permissions
check_permissions() {
    echo "🔐 Memeriksa File Permissions..."
    
    if [ -r "app.py" ]; then
        echo "✅ app.py bisa dibaca"
    else
        echo "❌ app.py tidak bisa dibaca"
        return 1
    fi
    
    if [ -x "cleanup.sh" ]; then
        echo "✅ cleanup.sh bisa dieksekusi"
    else
        echo "⚠️  cleanup.sh tidak bisa dieksekusi"
        chmod +x cleanup.sh
        echo "✅ Permissions diperbaiki"
    fi
    
    return 0
}

# Main health check
main() {
    local overall_health=true
    
    echo "🔍 Memulai health check..."
    echo ""
    
    check_python || overall_health=false
    echo ""
    
    check_venv || overall_health=false
    echo ""
    
    check_dependencies || overall_health=false
    echo ""
    
    check_port || overall_health=false
    echo ""
    
    check_folders || overall_health=false
    echo ""
    
    check_permissions || overall_health=false
    echo ""
    
    # Summary
    echo "📊 HASIL HEALTH CHECK:"
    echo "======================"
    
    if $overall_health; then
        echo "🎉 Aplikasi dalam kondisi SEHAT!"
        echo "✅ Siap untuk dijalankan"
    else
        echo "⚠️  Aplikasi memiliki beberapa masalah"
        echo "🔧 Perbaiki masalah di atas sebelum menjalankan"
    fi
    
    echo ""
    echo "💡 Tips:"
    echo "   - Jalankan cleanup.sh untuk membersihkan cache"
    echo "   - Jalankan auto_update.sh untuk update"
    echo "   - Pastikan semua dependencies terinstall"
}

# Jalankan health check
main
