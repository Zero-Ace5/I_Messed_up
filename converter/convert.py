import os
import uuid
import time
import threading
import subprocess
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "converted"
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"   # absolute path

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

progress_data = {}   # job_id → status dict


def delete_later(path, delay=300):
    time.sleep(delay)
    if os.path.exists(path):
        os.remove(path)


def convert_file_ffmpeg(input_path, output_path, job_id):
    progress_data[job_id]["progress"] = 0
    progress_data[job_id]["mode"] = "loading"   # default (no duration yet)

    cmd = [
        FFMPEG,
        "-y",
        "-i", input_path,
        "-progress", "pipe:1",
        "-nostats",
        output_path
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    duration = None

    for line in process.stdout:
        line = line.strip()

        # Detect duration once
        if "Duration:" in line and duration is None:
            try:
                t = line.split("Duration:")[1].split(",")[0].strip()
                h, m, s = t.split(":")
                duration = float(h) * 3600 + float(m) * 60 + float(s)
                progress_data[job_id]["mode"] = "video"
            except:
                pass

        # Detect ongoing progress
        if "out_time_ms=" in line:
            try:
                ms = int(line.split("=")[1])
                seconds = ms / 1_000_000

                if duration:
                    percent = int((seconds / duration) * 100)
                    progress_data[job_id]["progress"] = min(percent, 100)
            except:
                pass

    # ffmpeg finished
    progress_data[job_id]["progress"] = 100
    progress_data[job_id]["mode"] = "done"


@app.route("/")
def home():
    message = request.args.get("message")
    return render_template("c_index.html", message=message)


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("file")
    if not file:
        return redirect(url_for("home", message="No file uploaded"))

    target_format = request.form.get("format")
    if not target_format:
        return redirect(url_for("home", message="Select output format"))

    job_id = str(uuid.uuid4())

    # Save uploaded file
    input_name = f"{job_id}_{file.filename}"
    input_path = os.path.join(UPLOAD_DIR, input_name)
    file.save(input_path)

    # Output path
    base = os.path.splitext(file.filename)[0]
    output_name = f"{base}.{target_format}"
    output_path = os.path.join(OUTPUT_DIR, output_name)

    # Initialize job data
    progress_data[job_id] = {
        "progress": 0,
        "mode": "loading",
        "output": output_name
    }

    # Start conversion thread
    threading.Thread(
        target=convert_file_ffmpeg,
        args=(input_path, output_path, job_id),
        daemon=True
    ).start()

    return render_template("c_progress.html", job_id=job_id)


@app.route("/progress/<job_id>")
def progress(job_id):
    return jsonify(progress_data.get(job_id, {
        "progress": 0,
        "mode": "loading"
    }))


@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(OUTPUT_DIR, filename)

    # schedule deletion of output file
    threading.Thread(target=delete_later, args=(path,), daemon=True).start()

    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
