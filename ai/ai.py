from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import httpx

app = FastAPI(title="Mini AI powered by Hugging AI 💵")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
TOKEN = "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"


async def query(prompt: str):
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json",
            },
            json={"inputs": prompt},
        )
        if response.status_code != 200:
            return f"❤️We are f*cked bros, AI not responding {response.status_code}"

        data = response.json()
        try:
            return data[0]["generated_text"]
        except Exception:
            return str(data)


@app.get('/', response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Mini AI Chat</title>
        <style>
            body { font-family: Arial; background: #fafafa; text-align: center; padding: 40px; }
            h1 { color: #4A148C; }
            textarea { width: 80%; height: 100px; font-size: 16px; padding: 10px; }
            button { margin-top: 10px; padding: 10px 20px; font-size: 16px; background: #4A148C; color: white; border: none; cursor: pointer; }
            .response { margin-top: 30px; text-align: left; width: 80%; margin-left: auto; margin-right: auto; background: #f1f1f1; padding: 15px; border-radius: 8px; }
        </style>
    </head>
    <body>
         <h1>🤖 Mini AI Chat Assistant</h1>
         <form action="/ask" method="post">
            <textarea name="prompt" placeholder="Ask me anything..." required></textarea><br>
            <button type="submit">Ask</button>
        </form>
    </body>
    </html>
    """


@app.post("/ask", response_class=HTMLResponse)
async def ask(prompt: str = Form(...)):
    reply = await query(prompt)
    html = f"""
    <html>
    <head>
        <title>Mini AI Chat</title>
    </head>
    <body style="font-family: Arial; background: #fafafa; text-align:center; padding:40px;">
        <h1>🤖 Mini AI Chat Assistant</h1>
        <div class="response">
            <b>You:</b> {prompt}<br><br>
            <b>AI:</b> {reply}
        </div>
        <p><a href="/">Ask another</a></p>
    </body>
    </html>
    """
    return html
