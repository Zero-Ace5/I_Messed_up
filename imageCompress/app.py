import os
import uuid
import time
import threading
from flask import Flask, request, render_template, send_file
from PIL import Image

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "compressed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
# making directories

app = Flask(__name__)

AUTO_DELETE_SECONDS = 300


def delete_later(path):
    time.sleep(AUTO_DELETE_SECONDS)
    if os.path.exists(path):
        os.remove(path)
    # setting up auto delete


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        quality = int(request.form.get("quality", 60))

        # receiving form data

        if not file or file.filename == "":
            return render_template("index.html", error="No File Seniore!")
        # checking if form data was received or not

        ext = file.filename.rsplit(".", 1)[-1].lower()
        filename = uuid.uuid4().hex + "." + ext
        input_path = os.path.join(UPLOAD_DIR, filename)
        file.save(input_path)
        # generating file name and saving it

        output_path = os.path.join(OUTPUT_DIR, filename)

        img = Image.open(input_path)

        if ext in ["jpg", "jpeg"]:
            img = img.convert("RGB")
            img.save(output_path, "JPEG", optimize=True, quality=quality)
        elif ext == "png":
            img.save(output_path, "PNG", optimize=True)

        elif ext == "webp":
            img.save(output_path, "WEBP", quality=quality, method=6)

        else:
            img = img.convert("RGB")
            output_path = os.path.join(OUTPUT_DIR, uuid.uuid4().hex + ".jpg")
            img.save(output_path, "JPEG", optimize=True, quality=quality)
        # actual conversion

        threading.Thread(target=delete_later, args=(
            input_path,), daemon=True).start()
        threading.Thread(target=delete_later, args=(
            output_path,), daemon=True).start()
        # Scheduling delete tasks

        return render_template("result.html", file=filename)

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(OUTPUT_DIR, filename)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
