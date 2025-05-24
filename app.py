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

# Register HEIF opener to support HEIC
register_heif_opener()

app = Flask(__name__)
app.template_folder = 'templates'

# Define storage folders
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
DOWNLOAD_FOLDER = 'downloads'
CACHE_FOLDER = 'cache'

# Make sure folders exist
for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER, DOWNLOAD_FOLDER, CACHE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Cache for frequently accessed URLs
url_cache = {}

# Functions for Video Downloader
def clean_tiktok_title(title):
    # If hashtags (#) exist, take text before the first hashtag
    if '#' in title:
        title = title.split('#')[0].strip()
    
    # Remove unsafe characters for filenames
    title = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores
    title = re.sub(r'\s+', '_', title.strip())
    
    return title

def clean_instagram_title(info):
    # Try to get caption from info
    try:
        # Get caption or description
        caption = info.get('description', '') or info.get('title', '')
        # Clean unwanted characters and limit to 20 characters
        # Remove hashtags and mentions
        caption = re.sub(r'#\w+|@\w+', '', caption)
        # Remove unwanted characters, replace with underscore
        caption = re.sub(r'[^\w\s-]', '', caption)
        # Replace spaces with underscore
        caption = re.sub(r'\s+', '_', caption.strip())
        # Limit to 20 characters
        caption = caption[:20]
        # If caption is empty, use timestamp
        if not caption:
            caption = f"ig_video_{int(time.time())}"
        return caption
    except:
        # Fallback to timestamp if error occurs
        return f"ig_video_{int(time.time())}"

def clean_filename(filename):
    """Clean filename from disallowed characters"""
    # Replace special characters that might cause issues
    filename = filename.replace('"', '').replace(''', '').replace('"', '')
    filename = filename.replace(''', '').replace('＂', '').replace('：', '-')
    
    # Remove unsafe characters for filenames
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscore
    filename = re.sub(r'\s+', '_', filename.strip())
    # Make sure filename is not empty
    if not filename:
        filename = f"file_{int(time.time())}"
    return filename

def get_cache_key(url, platform, format_type):
    """Create unique cache key based on URL, platform, and format"""
    cache_string = f"{url}_{platform}_{format_type}"
    return hashlib.md5(cache_string.encode()).hexdigest()

def check_cache(cache_key):
    """Check if file already exists in cache"""
    cache_file = os.path.join(CACHE_FOLDER, f"{cache_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
            # Make sure file still exists
            if os.path.exists(cache_data['filename']):
                return cache_data
    return None

def save_to_cache(cache_key, data):
    """Save download result to cache"""
    cache_file = os.path.join(CACHE_FOLDER, f"{cache_key}.json")
    with open(cache_file, 'w') as f:
        json.dump(data, f)

def download_video(url, platform, format_type='mp4'):
    # Check cache first
    cache_key = get_cache_key(url, platform, format_type)
    cached_data = check_cache(cache_key)
    if cached_data:
        return cached_data
    
    # Configure ydl_opts based on platform
    if platform == 'instagram':
        ydl_opts = {
            'format': 'best',  # Changed from 'best[height<=720]' to 'best' to get any available format
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
        
        # If MP3 format is selected
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
            'format': 'best',  # Changed from 'best[height<=720]' to 'best' to get any available format
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
        
        # If MP3 format is selected
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
                # Limit maximum quality to 720p for faster download
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
                # Use caption or timestamp for filename
                new_title = clean_instagram_title(info)
                old_filename = f"{DOWNLOAD_FOLDER}/{info['title']}.mp4"
                new_filename = f"{DOWNLOAD_FOLDER}/{new_title}.mp4"
                
                # If file with the same name already exists, add timestamp
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
                # Clean YouTube title too
                original_title = title
                title = clean_filename(title)
                
                # If title changed, rename file
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
            
            # Make sure filename is clean from special characters
            title = clean_filename(title)
            
            extension = 'mp4'
            if format_type == 'mp3':
                extension = 'mp3'
                # For TikTok and Instagram, rename MP3 conversion result
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
            
            # Save to cache
            save_to_cache(cache_key, result)
            
            return result
    except Exception as e:
        error_message = str(e)
        
        # Provide clearer error messages and solution suggestions
        if "format is not available" in error_message:
            error_message = f"Video format not available. Please download from the original site."
        elif "Unsupported URL" in error_message or "This URL is not supported" in error_message:
            error_message = f"URL not supported. Please make sure the URL is valid for platform {platform}."
        elif "Sign in to confirm" in error_message or "Please log in or sign up" in error_message:
            error_message = f"This video requires login. Please download from the original site."
            
        return {
            'status': 'error',
            'message': error_message
        }

# Functions for Image Converter
def convert_image(input_path, output_path, target_format):
    """Converting images to specified format (HEIC/JPG/PNG to JPG/PNG/PDF)"""
    try:
        # For HEIC to other formats (JPG/PNG/PDF)
        if input_path.lower().endswith('.heic'):
            img = Image.open(input_path)
            # Convert color mode if needed
            if img.mode != 'RGB' and target_format.lower() != 'png':
                img = img.convert('RGB')
            
            # Specific handling for PDF conversion
            if target_format.lower() == 'pdf':
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output_path, format=target_format, resolution=100.0)
            else:
                img.save(output_path, format=target_format)
            return True
        # For other formats
        elif input_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            img = Image.open(input_path)
            # Convert to PDF
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
            print(f"Input file format not supported: {input_path}")
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
        # Check if request is JSON or form data
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
            return jsonify({'status': 'error', 'message': 'URL not found'}), 400
        
        # Check if format is valid (Remove MP3 restriction for YouTube)
        if format_type not in ['mp3', 'mp4']:
            format_type = 'mp4'  # default to mp4 if not valid
        
        # Check if platform is valid
        if platform not in ['youtube', 'tiktok', 'instagram']:
            platform = 'youtube'  # default to youtube if not valid
        
        result = download_video(url, platform, format_type)
        
        # If request is from form, render template with result
        if not request.is_json:
            if result['status'] == 'success':
                return render_template('index.html', 
                                      success=True, 
                                      download_path=result['title'])
            else:
                return render_template('index.html', 
                                      error=result['message'])
        
        # If request is JSON, return JSON
        return jsonify(result)
    except Exception as e:
        if request.is_json:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        else:
            return render_template('index.html', error=str(e))

@app.route('/get-video/<path:filename>')
def get_video(filename):
    try:
        # Remove 'downloads/' from filename if exists
        clean_filename = filename.replace(f'{DOWNLOAD_FOLDER}/', '')
        
        # Check if file exists, if not try to add extensions
        file_path = f'{DOWNLOAD_FOLDER}/{clean_filename}'
        if not os.path.exists(file_path):
            # Check if file with mp4 or mp3 extension exists
            if os.path.exists(f'{file_path}.mp4'):
                file_path = f'{file_path}.mp4'
                clean_filename = f'{clean_filename}.mp4'
            elif os.path.exists(f'{file_path}.mp3'):
                file_path = f'{file_path}.mp3'
                clean_filename = f'{clean_filename}.mp3'
            else:
                # Try to find a file with similar name in the downloads folder
                try:
                    for f in os.listdir(DOWNLOAD_FOLDER):
                        # Skip directories
                        if os.path.isdir(os.path.join(DOWNLOAD_FOLDER, f)):
                            continue
                            
                        # Check if the file name contains our search string (case insensitive)
                        if clean_filename.lower().replace('_', ' ') in f.lower():
                            file_path = os.path.join(DOWNLOAD_FOLDER, f)
                            clean_filename = f
                            break
                except Exception as e:
                    print(f"Error finding similar file: {e}")
        
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=clean_filename
            )
        else:
            return jsonify({'error': f'File not found: {clean_filename}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/open-folder')
def open_folder():
    try:
        folder_path = os.path.abspath(DOWNLOAD_FOLDER)
        subprocess.run(['open', folder_path])
        # Return minimal JSON response
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Image Converter Routes
@app.route('/convert-image', methods=['POST'])
def convert_image_api():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'File not found'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'})
    
    target_format = request.form.get('format', 'jpeg').lower()
    
    # Validate supported formats
    if target_format not in ['jpeg', 'png', 'pdf']:
        return jsonify({'status': 'error', 'message': 'Format not supported'})
    
    # Save uploaded file
    timestamp = int(time.time())
    original_filename = file.filename
    file_ext = Path(original_filename).suffix
    base_filename = Path(original_filename).stem
    
    upload_path = os.path.join(UPLOAD_FOLDER, f"{base_filename}_{timestamp}{file_ext}")
    file.save(upload_path)
    
    # Determine output path
    ext_map = {
        'jpeg': '.jpg',
        'png': '.png',
        'pdf': '.pdf'
    }
    
    output_filename = f"{base_filename}_{timestamp}{ext_map[target_format]}"
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)
    
    # Perform conversion
    success = convert_image(upload_path, output_path, target_format)
    
    if success:
        return jsonify({
            'status': 'success',
            'message': 'Conversion successful',
            'filename': output_filename,
            'download_url': f'/get-converted-image/{output_filename}'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Failed to convert image'
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