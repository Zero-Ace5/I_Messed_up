from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import ollama
import asyncio

app = FastAPI(title="Mini AI Chat (Offline Mistral 💬)")


async def query(prompt: str):
    try:
        def run_chat():
            response = ollama.chat(model="mistral", messages=[
                {"role": "system", "content": "You are a friendly and helpful assistant."},
                {"role": "user", "content": prompt}
            ])
            return response["message"]["content"]

        reply = await asyncio.to_thread(run_chat)
        return reply

    except Exception as e:
        return f"⚠️ Error contacting local Mistral model: {e}"


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Mini AI Chat (Offline)</title>
        <style>
            body { font-family: Arial; background: #fdfdfd; text-align: center; padding: 40px; }
            h1 { color: #2E86DE; }
            textarea { width: 80%; height: 120px; font-size: 16px; padding: 10px; border-radius: 6px; border: 1px solid #ccc; }
            button { margin-top: 10px; padding: 10px 20px; font-size: 16px; background: #2E86DE; color: white; border: none; cursor: pointer; border-radius: 6px; }
            .response { margin-top: 30px; text-align: left; width: 80%; margin-left: auto; margin-right: auto; background: #f1f1f1; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
         <h1>🤖 Mini AI Chat (Mistral - Local)</h1>
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
    <head><title>Mini AI Chat (Offline)</title></head>
    <body style="font-family: Arial; background: #fafafa; text-align:center; padding:40px;">
        <h1>🤖 Mini AI Chat (Mistral - Local)</h1>
        <div class="response">
            <b>You:</b> {prompt}<br><br>
            <b>AI:</b> {reply}
        </div>
        <p><a href="/">Ask another</a></p>
    </body>
    </html>
    """
    return html
