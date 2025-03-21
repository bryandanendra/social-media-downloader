import os
import sys
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    # Pastikan berada di direktori yang benar
    if getattr(sys, 'frozen', False):
        # Jika running sebagai bundled executable
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(application_path)
    
    # Buat folder downloads jika belum ada
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # Import dan jalankan aplikasi Flask
    from yt import app
    
    # Buka browser setelah 1.5 detik
    Timer(1.5, open_browser).start()
    
    # Jalankan server
    app.run(debug=False, host='127.0.0.1', port=8000) 