from flask import Flask, request, render_template

app = Flask(__name__)


def calculate(a, b, op):
    a = float(a)
    b = float(b)

    if op == "add":
        return a + b
    elif op == "sub":
        return a - b
    elif op == "mul":
        return a * b
    elif op == "div":
        if b == 0:
            return "Error: Cannot divide by Zero"
        return a / b

    return "Invalid Operations"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        a = request.form.get("a", "")
        b = request.form.get("b", "")
        op = request.form.get("op")

        try:
            float(a)
            float(b)
        except ValueError:
            error = "Please enter valid numbers"
            return render_template("index.html", error=error)

        result = calculate(a, b, op)

    return render_template("index.html", error=error, result=result)


if __name__ == "__main__":
    app.run(debug=True)
