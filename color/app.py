import random
from flask import Flask, render_template, request


app = Flask(__name__)


def generate_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


def generate_palette(n):
    return [generate_color() for _ in range(n)]


@app.route("/", methods=["GET", "POST"])
def index():
    colors = None

    if request.method == "POST":
        try:
            count = int(request.form.get("count", 5))
            if count < 1 or count > 50:
                count = 5
        except ValueError:
            count = 5

        colors = generate_palette(count)

    return render_template("index.html", colors=colors)


if __name__ == "__main__":
    app.run(debug=True)
