#!/bin/bash

# Clean App Bundle Script for Donverter
# Script ini akan menghapus app bundle yang dibuat oleh create_simple_app.sh

echo "🧹 Clean App Bundle Donverter"
echo "============================="
echo ""

# Dapatkan path direktori script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Direktori: $SCRIPT_DIR"
echo ""

# Cek apakah app bundle ada
if [ -d "Donverter.app" ]; then
    echo "📱 App bundle ditemukan: Donverter.app"
    echo "📊 Ukuran: $(du -sh Donverter.app | cut -f1)"
    echo ""
    
    echo "⚠️  PERINGATAN: Script ini akan menghapus Donverter.app"
    echo "💡 App bundle bisa dibuat ulang dengan: bash create_simple_app.sh"
    echo ""
    
    read -p "Apakah Anda yakin ingin menghapus Donverter.app? (y/N): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Menghapus Donverter.app..."
        rm -rf Donverter.app
        
        if [ ! -d "Donverter.app" ]; then
            echo "✅ Donverter.app berhasil dihapus"
        else
            echo "❌ Gagal menghapus Donverter.app"
        fi
    else
        echo "❌ Pembatalan: Donverter.app tidak dihapus"
    fi
else
    echo "✅ Donverter.app tidak ditemukan"
    echo "💡 Tidak ada yang perlu dibersihkan"
fi

echo ""
echo "🔍 Status direktori:"
ls -la | grep -E "(Donverter\.app|\.app)"

echo ""
echo "🎯 Clean up selesai!"
echo "💡 Untuk membuat app bundle baru:"
echo "   bash create_simple_app.sh"
