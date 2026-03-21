from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os, subprocess, datetime, json
from config import *

app = Flask(__name__)

# Historial de descargas
HISTORY_FILE = os.path.join(LOG_FOLDER, "history.json")
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
else:
    history = []

# 🚀 Guardar historial
def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# 🏠 HOME
@app.route('/')
def index():
    return render_template("index.html", history=history)

# 🔗 DESCARGAR POR LINK
@app.route('/link', methods=['GET','POST'])
def link_page():
    if request.method == 'POST':
        url = request.form.get("video_url")
        custom_name = request.form.get("custom_name", "")
        
        filename = custom_name.strip() if custom_name else "%(title)s.%(ext)s"
        output_path = os.path.join(DOWNLOAD_FOLDER, filename)

        try:
            subprocess.run([
                "yt-dlp",
                "-f", "best[ext=mp4]",
                "-o", output_path,
                url
            ], check=True)
        except subprocess.CalledProcessError:
            return "❌ Error descargando video"

        entry = {
            "url": url,
            "name": filename,
            "date": str(datetime.datetime.now())
        }
        history.append(entry)
        save_history()
        return redirect(url_for('history_page'))

    return render_template("link.html")

# 📜 HISTORIAL
@app.route('/history')
def history_page():
    return render_template("history.html", videos=history)

# 📥 DESCARGAR ARCHIVO LOCAL
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

# 🚀 INICIO
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)