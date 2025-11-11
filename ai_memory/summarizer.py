import json
import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


async def summarize_text(text: str):
    prompt = f"Summarize this clearly and concisely with start and end having a special mark for easy identification:\n\n{text[:4000]}"
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt})
        content = ""
        async for line in res.aiter_lines():
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                content += data.get("response", "")
                print(content)
            except:
                pass
    return content
