from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
import httpx
import json

app = FastAPI(title="Local Chat with Ollama 💬")

MODEL = "mistral"
URL = "http://localhost:11434/api/generate"
HISTORY = []


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>💬 Local Chat</title>
        <script src="https://unpkg.com/htmx.org@1.9.12"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                width: 80%;
                max-width: 800px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            .chat-box {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
            }
            .msg {
                margin: 10px 0;
                padding: 10px 15px;
                border-radius: 12px;
                max-width: 80%;
            }
            .user {
                background-color: #e1bee7;
                align-self: flex-end;
                text-align: right;
            }
            .bot {
                background-color: #dcedc8;
                align-self: flex-start;
            }
            form {
                display: flex;
                padding: 15px;
                background-color: #fafafa;
                border-top: 1px solid #ddd;
            }
            textarea {
                flex: 1;
                resize: none;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                height: 60px;
            }
            button {
                margin-left: 10px;
                background-color: #4A148C;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }
            button:hover {
                background-color: #6A1B9A;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div id="chat-box" class="chat-box">
                <!-- Chat messages go here -->
            </div>
            <form hx-post="/chat" hx-target="#chat-box" hx-swap="beforeend" hx-on::after-request="this.reset()">
                <textarea name="prompt" placeholder="Type your message..." required></textarea>
                <button type="submit">Send</button>
            </form>
        </div>

        <script>
            document.body.addEventListener('htmx:afterSwap', function() {
                const chatBox = document.getElementById('chat-box');
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        </script>
    </body>
    </html>
    """


@app.post("/chat", response_class=HTMLResponse)
async def chat(prompt: str = Form(...)):
    async def event_stream():
        yield f"<div class='msg user'>{prompt}</div>"

        try:
            conversation = "\n".join(
                [f"User: {m['user']}\nAssistant: {m['bot']}" for m in HISTORY]
            )
            full_prompt = f"""
### Instruction:
You are a helpful assistant. Continue this conversation naturally.

### Conversation:
{conversation}
User: {prompt}
Assistant:
"""

            yield "<div class='msg bot'>"
            bot_reply = ""

            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST", URL, json={"model": MODEL, "prompt": full_prompt}
                ) as response:
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        if line.startswith("{"):
                            try:
                                data = json.loads(line)
                                token = data.get("response", "")
                                bot_reply += token
                                yield token
                            except Exception:
                                continue

            yield "</div>"
            HISTORY.append({"user": prompt, "bot": bot_reply})

        except Exception as e:
            yield f"<p style='color:red;'>Error: {e}</p>"

    return StreamingResponse(event_stream(), media_type="text/html")
