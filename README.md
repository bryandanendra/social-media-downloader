# Video Downloader

Aplikasi web sederhana untuk mengunduh video dari YouTube, Instagram, dan TikTok. Dibuat dengan Python Flask dan antarmuka web modern menggunakan Tailwind CSS.

## Fitur

- ✨ Antarmuka pengguna yang modern dan responsif
- 🎥 Mendukung unduhan dari:
  - YouTube
  - Instagram
  - TikTok
- 🔍 Deteksi otomatis platform dari URL
- 📁 Tombol cepat untuk membuka folder unduhan
- 🎯 Pembersihan judul file otomatis
- 🔒 Berjalan secara lokal untuk keamanan

## Persyaratan

- Python 3.x
- Flask
- yt-dlp
- XAMPP (atau server web lainnya)
- PyInstaller (untuk membuat aplikasi desktop)

## Instalasi

1. Clone repositori ini atau download ke direktori web server Anda:
```bash
git clone [url-repositori]
```

2. Buat virtual environment dan aktifkan:
```bash
python -m venv venv
source venv/bin/activate  # Untuk Unix/macOS
# atau
venv\Scripts\activate  # Untuk Windows
```

3. Install dependensi yang diperlukan:
```bash
pip install flask yt-dlp pyinstaller
```

4. Jalankan aplikasi:
```bash
python yt.py
```

5. Buka browser dan akses:
```
http://127.0.0.1:8000
```

## Build Ulang Aplikasi Desktop

Jika Anda melakukan perubahan pada kode sumber, ikuti langkah-langkah berikut untuk build ulang aplikasi:

1. Pastikan berada di direktori project dan virtual environment aktif:
```bash
cd /Applications/XAMPP/xamppfiles/htdocs/ytdownloads
source venv/bin/activate
```

2. Build ulang aplikasi dengan PyInstaller:
```bash
pyinstaller app.spec
```

3. Pindahkan hasil build ke Applications:
```bash
cp -R "dist/YT Downloader" "/Applications/YT Downloader"
```

4. Jalankan aplikasi dari folder Applications

## Penggunaan

1. Buka aplikasi di browser
2. Paste URL video yang ingin diunduh
3. Platform akan terdeteksi otomatis
4. Klik tombol unduh
5. Tunggu proses unduhan selesai
6. Klik 'Save File' untuk menyimpan video
7. Atau klik tombol folder untuk membuka lokasi file

## Struktur Direktori

```
ytdownloads/
├── assets/           # Aset statis (gambar, ikon)
├── downloads/        # Folder penyimpanan hasil unduhan
├── venv/            # Virtual environment Python
├── index.html       # Antarmuka pengguna web
├── yt.py            # Aplikasi server Flask
├── run_app.py       # Script untuk menjalankan aplikasi desktop
└── app.spec         # Konfigurasi PyInstaller
```

## Catatan Keamanan

- Aplikasi ini berjalan secara lokal (localhost) untuk keamanan
- Pastikan untuk tidak membuka port 8000 ke jaringan publik
- Gunakan virtual environment untuk mengisolasi dependensi

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file LICENSE untuk detail.

## Kredit

Dibuat oleh @masbrii 