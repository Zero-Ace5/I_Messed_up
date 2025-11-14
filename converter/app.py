import os
import subprocess
import uuid
import threading
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "converted"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"   # absolute path


def convert_file(input_path, output_path):
    cmd = [
        FFMPEG,
        "-y",
        "-i", input_path,
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def delete_later(path, delay=300):
    import time
    time.sleep(delay)
    if os.path.exists(path):
        os.remove(path)


@app.route("/")
def home():
    message = request.args.get("message")
    return render_template("indexx.html", message=message)


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("file")
    if not file:
        return redirect(url_for("home", message="No file uploaded"))

    target_format = request.form.get("format")
    if not target_format:
        return redirect(url_for("home", message="Select output format"))

    # save input
    input_name = f"{uuid.uuid4()}_{file.filename}"
    input_path = os.path.join(UPLOAD_DIR, input_name)
    file.save(input_path)

    # output
    base = os.path.splitext(file.filename)[0]
    output_name = f"{base}.{target_format}"
    output_path = os.path.join(OUTPUT_DIR, output_name)

    # convert immediately (blocking)
    convert_file(input_path, output_path)

    # cleanup
    threading.Thread(target=delete_later, args=(
        input_path,), daemon=True).start()
    threading.Thread(target=delete_later, args=(
        output_path,), daemon=True).start()

    # return link
    dl = url_for("download", filename=output_name)
    msg = f"✅ Conversion complete: <a href='{dl}' download>Download</a>"

    return redirect(url_for("home", message=msg))


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
