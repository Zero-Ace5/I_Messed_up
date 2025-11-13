import os
import yt_dlp
import threading
import time
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory

app = Flask(__name__)
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Downloader</title>
</head>
<body style="font-family:sans-serif; text-align:center; margin-top:50px;">
    <h2>YouTube Downloader - 720p</h2>
    <form method="POST" action="/download">
        <input type="text" name="url" placeholder="Enter YouTube URL" size="50" required>
        <button type="submit">Download</button>
    </form>
    {% if message %}
        <p>{{ message|safe }}</p>
    {% endif %}
</body>
</html>
"""


@app.route('/', methods=['GET'])
def home():
    message = request.args.get("message")
    return render_template_string(HTML, message=message)


@app.route('/download', methods=['POST'])
def download():
    url = request.form["url"].strip()
    if not url.startswith("http"):
        return redirect(url_for("home", message="Invalid YouTube URL."))
    try:
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        settings = {
            "ffmpeg_location": r"C:\ffmpeg\bin",
            "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            "merge_output_format": "mp4",
            "postprocessor_args": ["-movflags", "faststart"],
            "restrictfilenames": True,
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(settings) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        file_only = os.path.basename(filename)
        download_url = url_for("save_file", filename=file_only)
        message = f"✅ Download successful: <a href='{download_url}' download>Click to save</a>"
        return redirect(url_for("home", message=message))
    except Exception as e:
        return render_template_string(HTML, message=f"Error:{e}")


@app.route("/downloads/<path:filename>")
def save_file(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)

    def delayed_delete(path):
        time.sleep(30)
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"Deleted Old File: {path}")
        except Exception as e:
            print(f"Delete File Error: {e}")
    threading.Thread(target=delayed_delete, args=(
        file_path,), daemon=True).start()
    return send_from_directory(DOWNLOAD_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
