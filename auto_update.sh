#!/bin/bash

# Donverter Auto Update Script
# Script untuk update otomatis dari GitHub

echo "🔄 Donverter Auto Update Script"
echo "================================"

# Dapatkan path direktori script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Fungsi untuk update
update_from_github() {
    echo "📥 Mengambil update terbaru dari GitHub..."
    
    # Stash perubahan lokal jika ada
    if ! git diff --quiet; then
        echo "💾 Menyimpan perubahan lokal..."
        git stash push -m "Auto update $(date)"
    fi
    
    # Pull update terbaru
    if git pull origin main; then
        echo "✅ Update berhasil!"
        
        # Restore perubahan lokal jika ada
        if git stash list | grep -q "Auto update"; then
            echo "🔄 Mengembalikan perubahan lokal..."
            git stash pop
        fi
        
        # Update dependencies jika ada
        if [ -f "requirements.txt" ]; then
            echo "📦 Mengupdate dependencies..."
            if [ -d "venv" ]; then
                source venv/bin/activate
                pip install -r requirements.txt --upgrade
            else
                pip3 install -r requirements.txt --upgrade
            fi
        fi
        
        echo "🎉 Update selesai! Silakan restart aplikasi."
    else
        echo "❌ Update gagal!"
        return 1
    fi
}

# Fungsi untuk check update
check_for_updates() {
    echo "🔍 Memeriksa update..."
    
    git fetch origin
    
    local local_commit=$(git rev-parse HEAD)
    local remote_commit=$(git rev-parse origin/main)
    
    if [ "$local_commit" != "$remote_commit" ]; then
        echo "📥 Ada update tersedia!"
        echo "   Local:  $(git log --oneline -1)"
        echo "   Remote: $(git log --oneline -1 origin/main)"
        
        read -p "Apakah Anda ingin update sekarang? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            update_from_github
        else
            echo "⏭️  Update dibatalkan."
        fi
    else
        echo "✅ Aplikasi sudah up-to-date!"
    fi
}

# Main menu
echo "Pilih opsi:"
echo "1. Check update"
echo "2. Update sekarang"
echo "3. Exit"
echo ""

read -p "Masukkan pilihan (1-3): " choice

case $choice in
    1)
        check_for_updates
        ;;
    2)
        update_from_github
        ;;
    3)
        echo "👋 Sampai jumpa!"
        exit 0
        ;;
    *)
        echo "❌ Pilihan tidak valid!"
        exit 1
        ;;
esac
