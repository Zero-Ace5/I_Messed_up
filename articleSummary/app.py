from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import requests
from bs4 import BeautifulSoup
import json
import subprocess

app = FastAPI(title="Article Summarizer 🤖")


def scraper(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        text = " ".join(paragraphs)

        return text if text else "No readable text"
    except Exception as e:
        return f"Page Error: {e}"


def summarize(text: str) -> str:
    try:
        prompt = f"Summarize this article clearly and concisely:\n\n{text[:3000]}"
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"
        return result.stdout.strip()
    except Exception as e:
        return f"Ollama Error: {e}"


@app.get('/', response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Article Summarizer</title>
        <style>
            body { font-family: Arial; background: #f4f4f4; text-align: center; padding: 50px; }
            h1 { color: #2E3A59; }
            input[type=text] { width: 70%; padding: 10px; border-radius: 6px; border: 1px solid #ccc; }
            button { padding: 10px 20px; margin-left: 10px; background: #2E3A59; color: white; border: none; border-radius: 6px; cursor: pointer; }
            .result { background: white; padding: 20px; margin-top: 40px; width: 70%; margin-left: auto; margin-right: auto; text-align: left; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <h1>📰 Article Summarizer</h1>
        <form action="/summarize/html" method="post">
            <input type="text" name="url" placeholder="Enter article URL" required>
            <button type="submit">Summarize</button>
        </form>
    </body>
    </html>
    """


@app.post("/summarize/html", response_class=HTMLResponse)
def summarizer(url: str = Form(...)):
    content = scraper(url)
    summary = summarize(content)

    return f"""
    <html>
    <head><title>Article Summary</title></head>
    <body style="font-family: Arial; background: #fdfdfd; padding: 40px;">
        <h2>🔗 Source:</h2>
        <p><a href="{url}" target="_blank">{url}</a></p>
        <h2>🧠 Summary:</h2>
        <div style="background:#f4f4f4;padding:15px;border-radius:8px;">{summary}</div>
        <h2>📄 Original Content:</h2>
        <div style="white-space: pre-wrap; background:#fafafa; padding:10px; border-radius:8px; max-height:300px; overflow-y:auto;">{content[:2000]}...</div>
        <p><a href="/">Summarize another article</a></p>
    </body>
    </html>
    """


@app.post("/summarize/json")
def summarizer_json(url: str = Form(...)):
    content = scraper(url)
    summary = summarize(content)
    return {"url": url, "summary": summary, "content_snippet": content[:1000]}
