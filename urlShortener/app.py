import string
import random
import sqlite3
from flask import Flask, render_template, redirect, request, url_for, abort

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS urls(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short TEXT UNIQUE NOT NULL,
        original TEXT NOT NULL,
        click INTEGER NOT NULL DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


init_db()


def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def create_unique_code():
    conn = get_db()
    cur = conn.cursor()

    while True:
        code = generate_code()
        cur.execute("SELECT 1 FROM urls WHERE short = ?", (code,))
        if cur.fetchone() is None:
            cur.close()
            return code


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        original = request.form.get("url", "").strip()

        if not original or not original.startswith(("https://", "http://")):
            return render_template("index.html", error="Invalid URL. Enter valid URL starting with https://")

        short = create_unique_code()

        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO urls (short, original) VALUES (?, ?)", (short, original))
        conn.commit()
        conn.close()

        short_link = url_for("redirect_short", code=short, _external=True)
        return render_template("created.html", short_link=short_link)
    return render_template("index.html")


@app.route("/u/<code>")
def redirect_short(code):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT original, click FROM urls WHERE short = ?", (code,))
    row = cur.fetchone()

    if not row:
        abort(404)

    new_clicks = row["click"] + 1
    cur.execute("UPDATE urls SET click = ? WHERE short = ?",
                (new_clicks, code))
    conn.commit()
    conn.close()

    return redirect(row["original"])


if __name__ == "__main__":
    app.run(debug=True)
