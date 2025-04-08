# Video Downloader - Panduan Instalasi Windows

Panduan lengkap cara menginstall dan menggunakan aplikasi Video Downloader di Windows. Ikuti langkah-langkah dengan urutan yang benar!

## Cara Penggunaan Singkat

1. Buka aplikasi dengan double-click pada file EXE atau shortcut di desktop
2. Paste URL video dari YouTube/Instagram/TikTok
3. Klik tombol download
4. Tunggu hingga proses selesai
5. File akan tersimpan di folder "downloads"

## Apa Yang Diperlukan

- [Python 3.x](https://www.python.org/downloads/) (Pastikan versi 3.8 atau lebih baru)
- [XAMPP](https://www.apachefriends.org/download.html) (Webserver)
- Git (opsional, hanya jika ingin menggunakan clone)

## Langkah Instalasi (Untuk Pemula)

### 1. Install Python

1. Download Python dari [python.org](https://www.python.org/downloads/)
2. **PENTING!** Saat instalasi, centang kotak "Add Python to PATH"
   ![Add Python to PATH](https://python-docs.readthedocs.io/en/latest/_images/win_installer.png)
3. Klik "Install Now"
4. Tunggu hingga proses instalasi selesai

### 2. Install XAMPP

1. Download XAMPP dari [apachefriends.org](https://www.apachefriends.org/download.html)
2. Jalankan installer dan ikuti petunjuk yang muncul
3. Install di lokasi default (`C:\xampp`)

### 3. Download Aplikasi

**Cara 1: Menggunakan Git** (untuk yang sudah familiar)
1. Buka Command Prompt atau PowerShell
2. Ketik perintah berikut:
   ```
   cd C:\xampp\htdocs
   git clone https://github.com/bryandanendra/social-media-downloader.git
   ```

**Cara 2: Download ZIP** (lebih mudah untuk pemula)
1. Kunjungi [https://github.com/bryandanendra/social-media-downloader](https://github.com/bryandanendra/social-media-downloader)
2. Klik tombol hijau "Code"
3. Pilih "Download ZIP"
4. Extract file ZIP ke folder `C:\xampp\htdocs\social-media-downloader`

### 4. Siapkan Aplikasi

1. Buka Command Prompt sebagai Administrator
   - Tekan tombol Windows
   - Ketik "cmd"
   - Klik kanan pada "Command Prompt" dan pilih "Run as administrator"

2. Masuk ke folder aplikasi:
   ```
   cd C:\xampp\htdocs\social-media-downloader
   ```

3. Buat dan aktifkan lingkungan virtual Python:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
   > Jika perintah python tidak dikenali, coba gunakan `py` sebagai gantinya

4. Install semua yang diperlukan:
   ```
   pip install -r requirements.txt
   ```
   > Proses ini mungkin memerlukan waktu beberapa menit, harap bersabar

## Menjalankan Aplikasi

### Cara Mudah (Mode Development)

1. Pastikan berada di folder aplikasi dan virtual environment aktif:
   ```
   cd C:\xampp\htdocs\social-media-downloader
   venv\Scripts\activate
   ```

2. Jalankan aplikasi:
   ```
   python app.py
   ```

3. Buka browser dan akses:
   ```
   http://127.0.0.1:8000
   ```

### Buat Aplikasi Desktop

Jika ingin membuat aplikasi yang bisa dibuka langsung tanpa Command Prompt:

1. Pastikan virtual environment aktif:
   ```
   cd C:\xampp\htdocs\social-media-downloader
   venv\Scripts\activate
   ```

2. Install PyInstaller jika belum:
   ```
   pip install pyinstaller
   ```

3. Build aplikasi:
   ```
   pyinstaller app.spec
   ```
   > Proses ini mungkin memerlukan waktu 5-10 menit

4. Copy hasil build:
   ```
   xcopy /E /I /Y "dist\YT Downloader" "C:\Program Files\YT Downloader"
   ```

5. Buat shortcut di Desktop:
   - Buka File Explorer
   - Buka folder `C:\Program Files\YT Downloader`
   - Klik kanan pada file `YT Downloader.exe`
   - Pilih "Create shortcut"
   - Drag shortcut ke Desktop

## Fitur Aplikasi

- ✨ Tampilan modern dan mudah digunakan
- 🎥 Download video dari:
  - YouTube (format MP4 dan MP3)
  - Instagram (Reels dan Post)
  - TikTok (Video)
- 🔍 Pendeteksian otomatis jenis platform
- 📁 Akses cepat ke folder hasil download
- 🖼️ Konverter gambar dari HEIC ke JPG/PNG

## Mengatasi Masalah Umum

### "Python not found" atau "Python tidak dikenali"
- Pastikan Python sudah di-install
- Pastikan sudah centang "Add Python to PATH" saat instalasi
- Restart komputer setelah menginstall Python
- Coba gunakan perintah `py` sebagai pengganti `python`

### Error saat instalasi package
- Pastikan Command Prompt dijalankan sebagai Administrator
- Pastikan koneksi internet stabil
- Update pip terlebih dahulu: `pip install --upgrade pip`
- Jika ada error pada paket tertentu, coba install satu per satu

### Aplikasi tidak bisa dibuka atau crash
- Pastikan antivirus tidak memblokir aplikasi
- Jalankan aplikasi sebagai Administrator
- Periksa Windows Event Viewer untuk detail error

### Tidak bisa akses folder downloads
- Jalankan aplikasi sebagai Administrator
- Periksa permission folder

## Bantuan & Dukungan

Jika mengalami masalah, silakan:
1. Buka issue di repository: https://github.com/bryandanendra/social-media-downloader/issues
2. Kontak @bryandanendra
3. Jalankan aplikasi melalui Command Prompt untuk melihat detail error 