import httpx
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


def _build_prompt(query: str, docs: list[str]) -> str:
    context = "\n\n".join(docs) if docs else "(no retrieved context)"
    return f"""You are a helpful assistant. Use the context to answer concisely. If the context is insufficient, say you don't know.

Context:
{context}

Question: {query}
Answer:"""


async def answer_query(query, memory) -> str:
    # 1) Retrieve relevant docs from Chroma
    try:
        # returns dict with 'documents' as list-of-lists
        results = memory.search(query, n=3)
        docs = results.get("documents", [[]])[0]
    except Exception:
        docs = []

    prompt = _build_prompt(query, docs)

    # 2) Call Ollama and parse streaming JSON lines
    async with httpx.AsyncClient(timeout=None) as client:
        res = await client.post(OLLAMA_URL, json={"model": MODEL, "prompt": prompt})
        raw = await res.aread()
        text = raw.decode().strip()

    parts = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
            if "response" in obj:
                parts.append(obj["response"])
        except json.JSONDecodeError:
            continue

    return "".join(parts).strip() or "No valid response from Ollama."
