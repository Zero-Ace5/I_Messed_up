import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI(title="Mini AI powered by AIML API 💬")
api_key = os.getenv("AIML_API_KEY")

if not api_key:
    raise ValueError("⚠️ AIML_API_KEY not found in .env file!")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.aimlapi.com/v1"
)


async def query(prompt: str):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error contacting AIML API: {e}"


# 🏠 Homepage
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Mini AI Chat</title>
        <style>
            body { font-family: Arial; background: #fdfdfd; text-align: center; padding: 40px; }
            h1 { color: #4A148C; }
            textarea { width: 80%; height: 100px; font-size: 16px; padding: 10px; }
            button { margin-top: 10px; padding: 10px 20px; font-size: 16px; background: #4A148C; color: white; border: none; cursor: pointer; border-radius: 6px; }
            .response { margin-top: 30px; text-align: left; width: 80%; margin-left: auto; margin-right: auto; background: #f1f1f1; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
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


# 💬 Chat endpoint
@app.post("/ask", response_class=HTMLResponse)
async def ask(prompt: str = Form(...)):
    reply = await query(prompt)
    html = f"""
    <html>
    <head><title>Mini AI Chat</title></head>
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
