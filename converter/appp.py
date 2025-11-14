import os
import threading
import time
import uuid
import subprocess
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, jsonify

app = Flask(__name__)
UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
OUTPUT_DIR = os.path.join(os.getcwd(), "converted")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Stores progress for active jobs
progress_data = {}
# Example:
# progress_data[job_id] = {"progress": 0, "output": "/path/to/file.mp4"}


def convert_file_ffmpeg(input_path, output_path, job_id):
    progress_data[job_id]["progress"] = 0

    command = [
        r"C:\ffmpeg\bin\ffmpeg.exe",  # FULL PATH HERE
        "-i", input_path,
        "-y",
        output_path,
        "-progress", "pipe:1",
        "-nostats"
    ]

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    duration = None
    for line in process.stdout:
        if "Duration" in line and duration is None:
            # Parse duration
            try:
                t = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = t.split(":")
                duration = float(h) * 3600 + float(m) * 60 + float(s)
            except:
                pass

        if "out_time_ms" in line:
            try:
                ms = int(line.split("=")[1].strip())
                seconds = ms / 1_000_000
                if duration:
                    progress = min(100, int((seconds / duration) * 100))
                    progress_data[job_id]["progress"] = progress
            except:
                pass

    progress_data[job_id]["progress"] = 100
    time.sleep(1)


@app.route("/", methods=["GET"])
def home():
    message = request.args.get("message")
    return render_template("index.html", message=message)


@app.route("/convert", methods=["POST"])
def convert():
    # file received
    file = request.files.get("file")
    if not file:
        return redirect(url_for("home", message="No file uploaded."))

    format = request.form.get("format")
    if not format:
        return redirect(url_for("home", message="No format selected."))

    job_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(input_path)

    base = os.path.splitext(file.filename)[0]
    output_filename = f"{base}.{format}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    progress_data[job_id] = {"progress": 0, "output": output_filename}

    threading.Thread(
        target=convert_file_ffmpeg,
        args=(input_path, output_path, job_id),
        daemon=True
    ).start()

    return render_template("progress.html", job_id=job_id)


@app.route("/progress/<job_id>")
def get_progress(job_id):
    return jsonify(progress_data.get(job_id, {"progress": 0}))


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
