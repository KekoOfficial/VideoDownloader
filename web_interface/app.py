from flask import Flask, render_template, request, redirect
from khassam import download_queue, log

app = Flask(__name__)

download_list = []

@app.route("/", methods=["GET", "POST"])
def index():
    global download_list
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            download_list.append(url)
        if "start" in request.form:
            download_queue(download_list)
            download_list = []
            return redirect("/")
    return render_template("index.html", queue=download_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)