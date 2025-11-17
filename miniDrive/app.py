import os
import uuid
import threading
import time
from flask import Flask, render_template, request, send_from_directory, abort, url_for

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)

AUTO_DELETE_SECONDS = 300


def delete_later(path, delay):
    time.sleep(delay)
    if os.path.exists(path):
        os.remove(path)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if not file or file.filename == "":
            return render_template("index.html", error="NO FILE ADDED.")

        ext = file.filename.rsplit(".", 1)[-1].lower()
        unique = uuid.uuid4().hex
        saved_name = f"{unique}.{ext}"

        path = os.path.join(UPLOAD_DIR, saved_name)
        file.save(path)

        if AUTO_DELETE_SECONDS:
            threading.Thread(target=delete_later, args=(
                path, AUTO_DELETE_SECONDS), daemon=True).start()

        share_url = url_for("download", file_id=saved_name, _external=True)
        return render_template("uploads.html", url=share_url)

    return render_template("index.html")


@app.route("/f/<file_id>")
def download(file_id):
    path = os.path.join(UPLOAD_DIR, file_id)
    if not os.path.exists(path):
        abort(404)

    return send_from_directory(UPLOAD_DIR, file_id, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
