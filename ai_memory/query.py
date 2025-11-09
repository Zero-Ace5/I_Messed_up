import httpx
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


async def answer_query(query, memory):
    prompt = f"""
You are a context-aware assistant.
Use the following memory and prior context to answer:

Memory:
{memory}

User question:
{query}
"""

    async with httpx.AsyncClient(timeout=None) as client:
        res = await client.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt})

        # Read the full streaming output
        raw = await res.aread()
        text = raw.decode().strip()
        print("🔍 DEBUG RAW RESPONSE FROM OLLAMA:\n", text, "\n" + "-" * 80)

        # Split the response into separate JSON objects
        lines = text.splitlines()
        responses = []

        for line in lines:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if "response" in obj:
                    responses.append(obj["response"])
            except json.JSONDecodeError:
                # Ignore malformed lines
                continue

        # Join all chunks into one coherent reply
        combined_response = "".join(responses).strip()

        return {
            "context": memory[:1000],  # optional small context preview
            "response": combined_response or "⚠️ No valid response from Ollama."
        }
