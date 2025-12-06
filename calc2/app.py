from flask import Flask, request, render_template
import operator
import ast

app = Flask(__name__)

ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}


def safe_eval(expr):
    def _eval(node):
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)

            if op_type in ops:
                if op_type is ast.Div and right == 0:
                    return "Error: Divide by Zero"
                return ops[op_type](left, right)

        elif isinstance(node, ast.Constant):
            return node.value

        return "Invalid Expression"

    try:
        parsed = ast.parse(expr, mode="eval")
        return _eval(parsed.body)
    except:
        return "Invalid Expression"


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        expr = request.form.get("expression", "")
        result = safe_eval(expr)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
