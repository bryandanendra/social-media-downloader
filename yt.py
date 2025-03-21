from flask import Flask, request, jsonify, send_file
from yt_dlp import YoutubeDL
import time
import os
import subprocess
import re

app = Flask(__name__)

def clean_tiktok_title(title):
    # Jika ada hashtag (#), ambil teks sebelum hashtag pertama
    if '#' in title:
        title = title.split('#')[0].strip()
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

def download_video(url, platform):
    if platform == 'instagram':
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'postprocessor_args': [
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
                '-c:a', 'aac', '-b:a', '128k', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart'
            ],
        }
    elif platform == 'tiktok':
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'extract_flat': False,
            'add_metadata': True,
            'postprocessor_args': [
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
                '-c:a', 'aac', '-b:a', '128k', '-pix_fmt', 'yuv420p',
                '-movflags', '+faststart'
            ],
        }
    else:  # youtube
        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'postprocessor_args': [
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '23',
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
                old_filename = f"downloads/{info['title']}.mp4"
                new_filename = f"downloads/{title}.mp4"
                if os.path.exists(old_filename):
                    os.rename(old_filename, new_filename)
            elif platform == 'instagram':
                # Gunakan caption atau timestamp untuk nama file
                new_title = clean_instagram_title(info)
                old_filename = f"downloads/{info['title']}.mp4"
                new_filename = f"downloads/{new_title}.mp4"
                
                # Jika file dengan nama yang sama sudah ada, tambahkan timestamp
                if os.path.exists(new_filename):
                    import time
                    new_title = f"{new_title}_{int(time.time())}"
                    new_filename = f"downloads/{new_title}.mp4"
                
                if os.path.exists(old_filename):
                    os.rename(old_filename, new_filename)
                title = new_title
            
            return {
                'status': 'success',
                'title': title,
                'filename': f"downloads/{title}.mp4"
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.json.get('url')
        platform = request.json.get('platform', 'youtube')  # default ke youtube jika tidak ada
        
        if not url:
            return jsonify({'status': 'error', 'message': 'URL tidak ditemukan'}), 400
        
        result = download_video(url, platform)
        return jsonify(result)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get-video/<path:filename>')
def get_video(filename):
    try:
        # Hapus 'downloads/' dari awal filename jika ada
        clean_filename = filename.replace('downloads/', '')
        return send_file(
            f'downloads/{clean_filename}',
            as_attachment=True,
            download_name=clean_filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/open-folder')
def open_folder():
    try:
        # folder_path = '/Applications/XAMPP/xamppfiles/htdocs/ytdownloads/downloads/'
        folder_path = '/Applications/YT Downloader/downloads/'
        subprocess.run(['open', folder_path])
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Buat folder downloads jika belum ada
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    # Jalankan server hanya di localhost untuk keamanan
    app.run(debug=True, host='127.0.0.1', port=8000)
