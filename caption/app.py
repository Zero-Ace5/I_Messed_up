import os
import uuid
from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUT_DIR = "generated"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


def get_font(img_width):
    size = max(20, img_width // 20)
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        top = request.form.get("top", "")
        bottom = request.form.get("bottom", "")

        if not file:
            render_template("index.html", error="No File Uploaded")

        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in ("jpg", "jpeg", "png"):
            render_template("index.html", error="Invalid File Type")

        filename = f"{uuid.uuid4().hex}.{ext}"
        input_path = os.path.join(UPLOAD_DIR, filename)
        file.save(input_path)

        img = Image.open(input_path).convert("RGB")
        draw = ImageDraw.Draw(img)

        font = get_font(img.width)

        if top.strip():
            draw.text((10, 10), top, font=font, fill="pink")

        if bottom.strip():
            bbox = font.getbbox(bottom)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            y = img.height - text_h - 10

            # Background rectangle
            draw.rectangle(
                (8, y - 2, 10 + text_w + 4, y + text_h + 2),
                fill="black")
            draw.text((10, y), bottom, font=font, fill="orange")

        out_name = f"{uuid.uuid4().hex}.jpg"
        out_path = os.path.join(OUT_DIR, out_name)
        img.save(out_path, "JPEG", quality=90)

        return render_template("result.html", filename=out_name)

    return render_template("index.html")


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(OUT_DIR, filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
