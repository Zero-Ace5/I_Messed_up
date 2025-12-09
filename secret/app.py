import os
import json
import secrets
import time
from flask import Flask, request, render_template, url_for

DATA_FILE = "data.json"

app = Flask(__name__)


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_secret(text, ttl_seconds=None):
    token = secrets.token_urlsafe(8)
    expires_at = int(time.time()) + int(ttl_seconds) if ttl_seconds else None
    data = load_data()
    data[token] = {"secret": text, "expires_at": expires_at}
    save_data(data)
    return token


def get_and_delete(token):
    data = load_data()
    entry = data.get(token)
    if not entry:
        return None
    if entry.get("expires_at") and int(time.time()) > int(entry["expires_at"]):
        del data[token]
        save_data(data)
        return None
    secret = entry.get("secret")
    del data[token]
    save_data(data)
    return secret


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("secret", "").strip()
        ttl = request.form.get("ttl_seconds", "").strip()
        if not text:
            return render_template("index.html", error="Enter a Secret")

        try:
            ttl_val = int(ttl) if ttl else None
        except ValueError:
            ttl_val = None

        token = create_secret(text, ttl_seconds=ttl_val)
        link = url_for("reveal", token=token, _external=True)
        return render_template("index.html", link=link, created=True)
    return render_template("index.html")


@app.route("/s/<token>")
def reveal(token):
    secret = get_and_delete(token)
    if secret is None:
        return render_template("reveal.html", missing=True)
    return render_template('reveal.html', secret=secret)


if __name__ == "__main__":
    app.run(debug=True)

# Questions (old program)
# what def _load_data() -> Dict[str, Any]: or def _save_data(data: Dict[str, Any]) -> None: do?
# what does  os.replace(tmp, DATA_FILE) do?
# Questions(new program)
# if entry.get("expires_at") and int(time.time()) > int(entry["expires_at"]):
# can't this be entry.get("expires_at") < int(time.time())
