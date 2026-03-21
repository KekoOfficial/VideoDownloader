from flask import Flask, render_template, request, redirect, url_for
import subprocess, os, datetime
from config import *

app = Flask(__name__)
history = []

def download_video(url):
    """Descarga el video usando yt-dlp en mp4"""
    temp_path = os.path.join(DOWNLOAD_FOLDER, "temp.mp4")
    cmd = ["yt-dlp", "-f", "best[ext=mp4]", url, "-o", temp_path]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return temp_path

def move_to_gallery(file_path):
    """Copia el archivo a la galería de Android y actualiza media scan"""
    filename = os.path.basename(file_path)
    gallery_path = os.path.join(GALLERY_FOLDER, filename)
    subprocess.run(["cp", file_path, gallery_path])
    subprocess.run([
        "am", "broadcast",
        "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
        "-d", f"file://{gallery_path}"
    ])
    return gallery_path

# ================== ROUTES ==================
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/link', methods=["POST"])
def link_download():
    url = request.form.get("video_url")
    if not url:
        return "❌ Ingresa un link válido"

    # Descargar
    temp_video = download_video(url)

    # Guardar en galería
    gallery_video = move_to_gallery(temp_video)

    # Guardar en historial
    history.append({
        "name": os.path.basename(gallery_video),
        "url": url,
        "date": str(datetime.datetime.now())
    })

    return redirect(url_for("history_page"))

@app.route('/history')
def history_page():
    return render_template("history.html", videos=history)

# ===========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)