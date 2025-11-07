import asyncio
import fitz
import httpx
import json
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import HTMLResponse

app = FastAPI(title="PDF Exporter...")

OLLAMA = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"


def extract(file) -> str:
    doc = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


async def check(chunk: str) -> str:
    prompt = f"Summarize the following text clearly and concisely:\n\n{chunk}"
    async with httpx.AsyncClient(timeout=120) as client:
        res = await client.post(
            OLLAMA_URL,
            json={"model": OLLAMA, "prompt": prompt}
        )
        content = ""
        async for line in res.aiter_lines():
            if line.strip():
                try:
                    data = json.loads(line)
                    content += data.get("response", "")
                except Exception:
                    pass
        return content


def chunk(text: str, max_len=2000):
    words = text.split()
    for i in range(0, len(words), max_len):
        yield " ".join(words[i:i+max_len])


async def summarize_pdf(file_bytes: bytes):
    text = extract(file_bytes)
    chunks = list(chunk(text))
    summaries = await asyncio.gather(*(check(c) for c in chunks))
    return '\n\n'.join(summaries)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>📄 Smart PDF Summarizer</title>
        <style>
            body { font-family: Arial; background-color: #f7f7f7; text-align: center; padding: 50px; }
            h1 { color: #333; }
            input, button { margin: 10px; padding: 10px; }
            .summary { background: #fff; border-radius: 8px; padding: 20px; width: 70%; margin: 20px auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: left; }
        </style>
    </head>
    <body>
        <h1>📄 Smart PDF Summarizer</h1>
        <form action="/summarize" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf" required><br>
            <button type="submit">Summarize PDF</button>
        </form>
    </body>
    </html>
    """


@app.post("/summarize", response_class=HTMLResponse)
async def summarize(file: UploadFile):
    try:
        file_bytes = await file.read()
        summary = await summarize_pdf(file_bytes)
        html = f"""
        <html>
        <head><title>📄 Summary Result</title></head>
        <body style="font-family:Arial;padding:40px;background:#fafafa;">
            <h1>🧠 Summary of {file.filename}</h1>
            <div class="summary">{summary}</div>
            <p><a href="/">Upload another PDF</a></p>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"<h2>Error processing PDF: {e}</h2>"
