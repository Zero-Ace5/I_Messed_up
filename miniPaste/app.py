import os
import uuid
from flask import Flask, render_template, redirect, abort, request, url_for

app = Flask(__name__)

PASTE_DIR = "pastes"
os.makedirs(PASTE_DIR, exist_ok=True)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if not text:
            return render_template("index.html", error="Can't share a empty file.")

        paste_id = uuid.uuid4().hex[:8]
        file_path = os.path.join(PASTE_DIR, paste_id + ".txt")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

        return redirect(url_for("view_paste", paste_id=paste_id))

    return render_template("index.html")


@app.route("/p/<paste_id>")
def view_paste(paste_id):
    file_path = os.path.join(PASTE_DIR, paste_id + ".txt")

    if not os.path.exists(file_path):
        abort(404)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return render_template("paste.html", content=content, paste_id=paste_id)


if __name__ == "__main__":
    app.run(debug=True)
