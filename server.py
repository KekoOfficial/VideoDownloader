from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS = os.path.join(BASE_DIR, "downloads")

os.makedirs(DOWNLOADS, exist_ok=True)

history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/link", methods=["POST"])
def link():
    url = request.form.get("url")

    if not url:
        return redirect(url_for("index"))

    output_path = os.path.join(DOWNLOADS, "video.mp4")

    # 🔥 Descargar video con nombre fijo
    command = f'yt-dlp -o "{output_path}" "{url}"'
    os.system(command)

    if os.path.exists(output_path):
        history.append(output_path)
        print("✅ Video descargado correctamente")
    else:
        print("❌ Error: video no encontrado")

    return redirect(url_for("index"))

@app.route("/history")
def show_history():
    return render_template("history.html", history=history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)