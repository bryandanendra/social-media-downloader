# Video Downloader - Panduan Windows

Panduan instalasi dan build aplikasi Video Downloader untuk sistem operasi Windows.

## Persyaratan

- Python 3.x (Download dari [python.org](https://www.python.org/downloads/))
- XAMPP (Download dari [apachefriends.org](https://www.apachefriends.org/download.html))
- Git (opsional, untuk clone repository)

## Instalasi

1. Install Python 3.x
   - Download Python dari [python.org](https://www.python.org/downloads/)
   - Saat instalasi, **PASTIKAN** centang opsi "Add Python to PATH"
   - Klik "Install Now"

2. Install XAMPP
   - Download XAMPP dari [apachefriends.org](https://www.apachefriends.org/download.html)
   - Install di lokasi default (`C:\xampp`)

3. Download atau Clone Repository
   ```bash
   # Jika menggunakan Git:
   cd C:\xampp\htdocs
   git clone [url-repositori] ytdownloads

   # Jika tidak menggunakan Git:
   # Download ZIP dan extract ke C:\xampp\htdocs\ytdownloads
   ```

4. Buka Command Prompt sebagai Administrator
   - Tekan Win + X
   - Pilih "Windows Terminal (Admin)" atau "Command Prompt (Admin)"

5. Buat dan aktifkan virtual environment:
   ```bash
   cd C:\xampp\htdocs\ytdownloads
   python -m venv venv
   venv\Scripts\activate
   ```

6. Install dependensi yang diperlukan:
   ```bash
   pip install flask yt-dlp pyinstaller
   ```

## Build Aplikasi Desktop

1. Pastikan virtual environment aktif:
   ```bash
   cd C:\xampp\htdocs\ytdownloads
   venv\Scripts\activate
   ```

2. Build aplikasi dengan PyInstaller:
   ```bash
   pyinstaller app.spec
   ```

3. Pindahkan hasil build ke Program Files:
   ```bash
   # Buat folder jika belum ada
   mkdir "C:\Program Files\YT Downloader"
   
   # Copy hasil build
   xcopy /E /I /Y "dist\YT Downloader" "C:\Program Files\YT Downloader"
   ```

4. Buat shortcut di Desktop (Opsional):
   - Buka File Explorer
   - Navigasi ke `C:\Program Files\YT Downloader`
   - Klik kanan pada file `YT Downloader.exe`
   - Pilih "Create shortcut"
   - Drag shortcut ke Desktop

## Menjalankan Aplikasi

### Cara 1: Dari Program Files
1. Buka File Explorer
2. Navigasi ke `C:\Program Files\YT Downloader`
3. Double-click `YT Downloader.exe`

### Cara 2: Dari Shortcut
- Double-click shortcut di Desktop (jika sudah dibuat)

### Cara 3: Development Mode
```bash
cd C:\xampp\htdocs\ytdownloads
venv\Scripts\activate
python yt.py
```

## Troubleshooting

1. Jika muncul error "python not found":
   - Pastikan Python sudah di-install
   - Pastikan Python sudah ditambahkan ke PATH
   - Restart Command Prompt

2. Jika muncul error saat instalasi package:
   - Jalankan Command Prompt sebagai Administrator
   - Pastikan internet stabil
   - Coba gunakan: `pip install --upgrade pip`

3. Jika aplikasi tidak bisa dibuka:
   - Pastikan antivirus tidak memblokir aplikasi
   - Coba jalankan sebagai Administrator
   - Periksa Windows Event Viewer untuk detail error

4. Jika folder downloads tidak bisa diakses:
   - Pastikan aplikasi dijalankan sebagai Administrator
   - Periksa permission folder

## Catatan Penting

- Pastikan XAMPP tidak menggunakan port 8000
- Jika ingin mengubah port, edit file `run_app.py`
- Folder downloads akan dibuat otomatis di lokasi aplikasi
- Untuk update aplikasi, ulangi proses build dan replace files di Program Files

## Bantuan

Jika mengalami masalah, bisa:
1. Buka issue di repository
2. Kontak @masbrii
3. Jalankan dalam mode development untuk melihat error detail 