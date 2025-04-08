# Video Downloader

Aplikasi web sederhana untuk mengunduh video dari YouTube, Instagram, dan TikTok. Dibuat dengan Python Flask dan antarmuka web modern menggunakan Tailwind CSS.

## Fitur

- ✨ Antarmuka pengguna yang modern dan responsif
- 🎥 Mendukung unduhan dari:
  - YouTube (format MP4 dan MP3)
  - Instagram (Reels dan Post)
  - TikTok (Video)
- 🔍 Deteksi otomatis platform dari URL yang ditempel
- 📁 Tombol cepat untuk membuka folder unduhan
- 🎯 Pembersihan judul file otomatis
- 🔒 Berjalan secara lokal untuk keamanan (tidak perlu internet untuk menjalankan aplikasi)
- 🖼️ Konverter gambar terintegrasi (termasuk dukungan HEIC untuk iPhone)

## Tampilan UI

![Tampilan UI Aplikasi](UI.png)

## Cara Penggunaan Singkat

1. Buka aplikasi di browser (http://127.0.0.1:8000)
2. Paste URL video yang ingin diunduh
3. Platform akan terdeteksi otomatis
4. Klik tombol unduh
5. Tunggu proses unduhan selesai
6. File akan tersimpan di folder "downloads"

## Persyaratan Sistem

Untuk pengguna **macOS & Linux**:
- Python 3.x
- XAMPP atau server web lainnya

**Catatan**: Untuk pengguna Windows, silakan lihat [README_WINDOWS.md](README_WINDOWS.md)

## Cara Instalasi (macOS & Linux)

1. Download atau clone repositori ini:
```bash
git clone https://github.com/bryandanendra/social-media-downloader.git
```

2. Buat virtual environment dan aktifkan:
```bash
python -m venv venv
source venv/bin/activate  # Untuk Unix/macOS
```

3. Install semua yang diperlukan:
```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi:
```bash
python app.py
```

5. Buka browser dan akses alamat berikut:
```
http://127.0.0.1:8000
```

## Membuat Aplikasi Desktop (Opsional)

Jika ingin membuat aplikasi yang bisa dibuka langsung tanpa terminal, ikuti langkah berikut:

1. Pastikan berada di direktori project dan virtual environment aktif:
```bash
cd /Applications/XAMPP/xamppfiles/htdocs/social-media-downloader
source venv/bin/activate
```

2. Build aplikasi dengan PyInstaller:
```bash
pyinstaller app.spec
```

3. Pindahkan hasil build ke Applications:
```bash
cp -R "dist/YT Downloader" "/Applications/YT Downloader"
```

4. Jalankan aplikasi dari folder Applications

## Menggunakan Konverter Gambar

Aplikasi ini juga memiliki fitur untuk mengubah format gambar:
1. Klik menu "Image Converter" di aplikasi
2. Upload gambar (termasuk format HEIC dari iPhone)
3. Pilih format output (JPG, PNG, dll)
4. Klik 'Convert' untuk mengubah format gambar
5. Download hasil konversi

## Struktur Folder

```
social-media-downloader/
├── cache/            # Cache untuk URL yang sering diakses
├── downloads/        # Folder penyimpanan hasil unduhan
├── uploads/          # Folder untuk file upload (konverter gambar)
├── converted/        # Folder untuk hasil konversi gambar
├── templates/        # Template HTML
├── venv/             # Virtual environment Python
├── app.py            # Aplikasi server Flask
├── run_app.py        # Script untuk menjalankan aplikasi desktop
├── requirements.txt  # Daftar dependensi
└── app.spec          # Konfigurasi PyInstaller
```

## Catatan Penting

- Aplikasi ini berjalan secara lokal (localhost) untuk keamanan
- Pastikan port 8000 tidak digunakan oleh aplikasi lain
- Gunakan virtual environment untuk mengisolasi dependensi
- Folder downloads, uploads, dan converted akan dibuat otomatis

## Bantuan & Dukungan

Jika mengalami masalah, silakan:
1. Buka issue di repository: https://github.com/bryandanendra/social-media-downloader/issues
2. Kontak @bryandanendra
3. Jalankan aplikasi melalui terminal untuk melihat pesan error

## Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file LICENSE untuk detail.

## Kredit

Dibuat oleh @bryandanendra 