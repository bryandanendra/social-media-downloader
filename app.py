from flask import Flask, request, jsonify, send_file, render_template
from yt_dlp import YoutubeDL
import time
import os
import subprocess
import re
from PIL import Image
from pillow_heif import register_heif_opener
from pathlib import Path
import hashlib
import json

# Register HEIF opener untuk support HEIC
register_heif_opener()

app = Flask(__name__)
app.template_folder = 'templates'

# Definisikan folder penyimpanan
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
DOWNLOAD_FOLDER = 'downloads'
CACHE_FOLDER = 'cache'

# Pastikan folder ada
for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER, DOWNLOAD_FOLDER, CACHE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Cache untuk URL yang sering diakses
url_cache = {}

# Fungsi untuk Video Downloader
def clean_tiktok_title(title):
    # Jika ada hashtag (#), ambil teks sebelum hashtag pertama
    if '#' in title:
        title = title.split('#')[0].strip()
    
    # Hapus karakter yang tidak aman untuk nama file
    title = re.sub(r'[^\w\s-]', '', title)
    # Ganti spasi dengan underscore
    title = re.sub(r'\s+', '_', title.strip())
    
    return title

def clean_instagram_title(info):
    # Coba ambil caption dari info
    try:
        # Ambil caption atau description
        caption = info.get('description', '') or info.get('title', '')
        # Bersihkan dari karakter yang tidak diinginkan dan batasi 20 karakter
        # Hapus hashtag dan mention
        caption = re.sub(r'#\w+|@\w+', '', caption)
        # Hapus karakter yang tidak diinginkan, ganti dengan underscore
        caption = re.sub(r'[^\w\s-]', '', caption)
        # Ganti spasi dengan underscore
        caption = re.sub(r'\s+', '_', caption.strip())
        # Batasi 20 karakter
        caption = caption[:20]
        # Jika caption kosong, gunakan timestamp
        if not caption:
            caption = f"ig_video_{int(time.time())}"
        return caption
    except:
        # Fallback ke timestamp jika terjadi error
        return f"ig_video_{int(time.time())}"

def clean_filename(filename):
    """Membersihkan nama file dari karakter yang tidak diizinkan"""
    # Hapus karakter yang tidak aman untuk nama file
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Ganti spasi dengan underscore
    filename = re.sub(r'\s+', '_', filename.strip())
    # Pastikan nama file tidak kosong
    if not filename:
        filename = f"file_{int(time.time())}"
    return filename

def get_cache_key(url, platform, format_type):
    """Membuat cache key unik berdasarkan URL, platform, dan format"""
    cache_string = f"{url}_{platform}_{format_type}"
    return hashlib.md5(cache_string.encode()).hexdigest()

def check_cache(cache_key):
    """Cek apakah file sudah ada di cache"""
    cache_file = os.path.join(CACHE_FOLDER, f"{cache_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            # Pastikan file masih ada
            if os.path.exists(cache_data['filename']):
                return cache_data
    return None

def save_to_cache(cache_key, data):
    """Simpan hasil download ke cache"""
    cache_file = os.path.join(CACHE_FOLDER, f"{cache_key}.json")
    with open(cache_file, 'w') as f:
        json.dump(data, f)

def download_video(url, platform, format_type='mp4'):
    # Cek cache dulu
    cache_key = get_cache_key(url, platform, format_type)
    cached_data = check_cache(cache_key)
    if cached_data:
        return cached_data
    
    # Konfigurasikan ydl_opts berdasarkan platform
    if platform == 'instagram':
        ydl_opts = {
            'format': 'best',  # Ubah dari 'best[height<=720]' ke 'best' untuk mendapatkan format apapun yang tersedia
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'postprocessor_args': [
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
                '-c:a', 'aac', '-b:a', '128k', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart'
            ],
        }
        
        # Jika format MP3 dipilih
        if format_type == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
    elif platform == 'tiktok':
        ydl_opts = {
            'format': 'best',  # Ubah dari 'best[height<=720]' ke 'best' untuk mendapatkan format apapun yang tersedia
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'extract_flat': False,
            'add_metadata': True,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'postprocessor_args': [
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
                '-c:a', 'aac', '-b:a', '128k', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart'
            ],
        }
        
        # Jika format MP3 dipilih
        if format_type == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
    else:  # youtube
        if format_type == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else: # mp4
            ydl_opts = {
                # Batasi kualitas maksimum 720p untuk lebih cepat
                'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                'postprocessor_args': [
                    '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
                    '-c:a', 'aac', '-b:a', '128k', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart'
                ],
            }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info['title']
            
            if platform == 'tiktok':
                title = clean_tiktok_title(title)
                old_filename = f"{DOWNLOAD_FOLDER}/{info['title']}.mp4"
                new_filename = f"{DOWNLOAD_FOLDER}/{title}.mp4"
                try:
                    if os.path.exists(old_filename):
                        os.rename(old_filename, new_filename)
                except Exception as e:
                    print(f"Error renaming TikTok file: {e}")
            elif platform == 'instagram':
                # Gunakan caption atau timestamp untuk nama file
                new_title = clean_instagram_title(info)
                old_filename = f"{DOWNLOAD_FOLDER}/{info['title']}.mp4"
                new_filename = f"{DOWNLOAD_FOLDER}/{new_title}.mp4"
                
                # Jika file dengan nama yang sama sudah ada, tambahkan timestamp
                if os.path.exists(new_filename):
                    import time
                    new_title = f"{new_title}_{int(time.time())}"
                    new_filename = f"{DOWNLOAD_FOLDER}/{new_title}.mp4"
                
                try:
                    if os.path.exists(old_filename):
                        os.rename(old_filename, new_filename)
                except Exception as e:
                    print(f"Error renaming Instagram file: {e}")
                title = new_title
            elif platform == 'youtube':
                # Bersihkan judul YouTube juga
                original_title = title
                title = clean_filename(title)
                
                # Jika judul berubah, rename file
                if original_title != title:
                    extension = "mp4"
                    if format_type == "mp3":
                        extension = "mp3"
                    
                    old_filename = f"{DOWNLOAD_FOLDER}/{original_title}.{extension}"
                    new_filename = f"{DOWNLOAD_FOLDER}/{title}.{extension}"
                    
                    try:
                        if os.path.exists(old_filename):
                            os.rename(old_filename, new_filename)
                    except Exception as e:
                        print(f"Error renaming YouTube file: {e}")
            
            # Pastikan nama file bersih dari karakter khusus
            title = clean_filename(title)
            
            extension = 'mp4'
            if format_type == 'mp3':
                extension = 'mp3'
                # Untuk TikTok dan Instagram, rename file hasil konversi MP3
                if platform in ['tiktok', 'instagram']:
                    mp3_old_filename = f"{DOWNLOAD_FOLDER}/{info['title']}.mp3"
                    mp3_new_filename = f"{DOWNLOAD_FOLDER}/{title}.mp3"
                    try:
                        if os.path.exists(mp3_old_filename) and mp3_old_filename != mp3_new_filename:
                            os.rename(mp3_old_filename, mp3_new_filename)
                    except Exception as e:
                        print(f"Error renaming MP3 file: {e}")
            
            result = {
                'status': 'success',
                'title': title,
                'filename': f"{DOWNLOAD_FOLDER}/{title}.{extension}"
            }
            
            # Simpan ke cache
            save_to_cache(cache_key, result)
            
            return result
    except Exception as e:
        error_message = str(e)
        
        # Berikan pesan error yang lebih jelas dan saran solusi
        if "format is not available" in error_message:
            error_message = f"Format video tidak tersedia. Coba unduh dari situs asli."
        elif "Unsupported URL" in error_message or "This URL is not supported" in error_message:
            error_message = f"URL tidak didukung. Pastikan URL valid untuk platform {platform}."
        elif "Sign in to confirm" in error_message or "Please log in or sign up" in error_message:
            error_message = f"Video ini memerlukan login. Coba unduh dari situs asli."
            
        return {
            'status': 'error',
            'message': error_message
        }

# Fungsi untuk Image Converter
def convert_image(input_path, output_path, target_format):
    """Mengkonversi gambar ke format yang ditentukan"""
    try:
        # Untuk HEIC ke format lain
        if input_path.lower().endswith('.heic'):
            img = Image.open(input_path)
            # Konversi mode warna jika perlu
            if img.mode != 'RGB' and target_format.lower() != 'png':
                img = img.convert('RGB')
            img.save(output_path, format=target_format)
            return True
        # Untuk format lain
        elif input_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            img = Image.open(input_path)
            # Konversi ke PDF
            if target_format.lower() == 'pdf':
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, format=target_format, resolution=100.0)
            else:
                if img.mode != 'RGB' and target_format.lower() != 'png':
                    img = img.convert('RGB')
                img.save(output_path, format=target_format)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error converting image: {e}")
        return False

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/image-converter')
def image_converter():
    return render_template('image_converter.html')

# Video Downloader Routes
@app.route('/download', methods=['POST'])
def download():
    try:
        # Cek apakah request JSON atau form data
        if request.is_json:
            data = request.json
            url = data.get('url')
            platform = data.get('platform', 'youtube') 
            format_type = data.get('format_type', 'mp4')
        else:
            url = request.form.get('url')
            platform = request.form.get('platform', 'youtube')
            format_type = request.form.get('format', 'mp4')
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL tidak ditemukan'}), 400
        
        # Cek apakah format valid (Hapus batas MP3 hanya untuk YouTube)
        if format_type not in ['mp3', 'mp4']:
            format_type = 'mp4'  # default ke mp4 jika tidak valid
        
        # Cek apakah platform valid
        if platform not in ['youtube', 'tiktok', 'instagram']:
            platform = 'youtube'  # default ke youtube jika tidak valid
        
        result = download_video(url, platform, format_type)
        
        # Jika request dari form, render template dengan hasil
        if not request.is_json:
            if result['status'] == 'success':
                return render_template('index.html', 
                                      success=True, 
                                      download_path=result['filename'].replace(DOWNLOAD_FOLDER+'/', ''))
            else:
                return render_template('index.html', 
                                      error=result['message'])
        
        # Jika request JSON, return JSON
        return jsonify(result)
    except Exception as e:
        if request.is_json:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            return render_template('index.html', error=str(e))

@app.route('/get-video/<path:filename>')
def get_video(filename):
    try:
        # Hapus 'downloads/' dari awal filename jika ada
        clean_filename = filename.replace(f'{DOWNLOAD_FOLDER}/', '')
        return send_file(
            f'{DOWNLOAD_FOLDER}/{clean_filename}',
            as_attachment=True,
            download_name=clean_filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/open-folder')
def open_folder():
    try:
        folder_path = os.path.abspath(DOWNLOAD_FOLDER)
        subprocess.run(['open', folder_path])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Image Converter Routes
@app.route('/convert-image', methods=['POST'])
def convert_image_api():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'File tidak ditemukan'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'Tidak ada file yang dipilih'})
    
    target_format = request.form.get('format', 'jpeg').lower()
    
    # Validasi format yang didukung
    if target_format not in ['jpeg', 'png', 'pdf']:
        return jsonify({'status': 'error', 'message': 'Format tidak didukung'})
    
    # Simpan file yang diupload
    timestamp = int(time.time())
    original_filename = file.filename
    file_ext = Path(original_filename).suffix
    base_filename = Path(original_filename).stem
    
    upload_path = os.path.join(UPLOAD_FOLDER, f"{base_filename}_{timestamp}{file_ext}")
    file.save(upload_path)
    
    # Tentukan path output
    ext_map = {
        'jpeg': '.jpg',
        'png': '.png',
        'pdf': '.pdf'
    }
    
    output_filename = f"{base_filename}_{timestamp}{ext_map[target_format]}"
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)
    
    # Lakukan konversi
    success = convert_image(upload_path, output_path, target_format)
    
    if success:
        return jsonify({
            'status': 'success',
            'message': 'Konversi berhasil',
            'filename': output_filename,
            'download_url': f'/get-converted-image/{output_filename}'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Gagal mengkonversi gambar'
        })

@app.route('/get-converted-image/<filename>')
def get_converted_image(filename):
    try:
        return send_file(
            os.path.join(CONVERTED_FOLDER, filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8060) 