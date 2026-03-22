from flask import Flask, render_template, request, redirect, url_for
from core.downloader import download_video

app = Flask(__name__)
history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/link", methods=["POST"])
def link():
    url = request.form.get("url")
    if url:
        download_video(url)  # descarga + galería
        history.append(url)
    return redirect(url_for("index"))

@app.route("/history")
def show_history():
    return render_template("history.html", history=history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)