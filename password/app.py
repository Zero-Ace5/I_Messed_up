from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import re

app = FastAPI(title="Password Strength Checker...")


def check(password: str):
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1

    if score <= 2:
        strength = "Weak"
    elif score == 4 or score == 3:
        strength = "Moderate"
    else:
        strength = "Strong"

    return {"password": password, "score": score, "strength": strength}


class Input(BaseModel):
    password: str


@app.post("/check")
def check_pass(data: Input):
    return check(data.password)


@app.get("/check/html", response_class=HTMLResponse)
def form_page():
    html = """
    <html>
    <head>
        <title>Password Strength Checker</title>
        <style>
            body { font-family: Arial; background-color: #f9f9f9; text-align: center; padding: 50px; }
            h1 { color: #333; }
            form { margin: 20px auto; width: 300px; }
            input[type=text] { width: 100%; padding: 8px; margin: 10px 0; }
            button { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer; }
            .result { font-size: 1.2em; margin-top: 20px; }
        </style>
    </head>
    <body>
         <h1>🔐 Password Strength Checker</h1>
         <form action="/check/html" method="post">
            <input type="text" name="password" placeholder="Enter password" required>
            <button type="submit">Check Strength</button>
         </form>
    </body>
    </html>
    """
    return html


@app.post("/check/html", response_class=HTMLResponse)
def check_page(password: str = Form(...)):
    result = check(password)
    html = f"""
    <html>
    <head>
        <title>Password Result</title>
        <style>
            body {{ font-family: Arial; background-color: #f9f9f9; text-align: center; padding: 50px; }}
            h1 {{ color: #333; }}
            .weak {{ color: red; }}
            .moderate {{ color: orange; }}
            .strong {{ color: green; }}
        </style>
    </head>
    <body>
        <h1>Result for: {result['password']}</h1>
        <p class="{result['strength'].lower()}">Strength: <b>{result['strength']}</b></p>
        <a href="/check/html">Go back</a>
    </body>
    </html>
    """

    return html
