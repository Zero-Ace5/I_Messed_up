import asyncio
from fetcher import fetch_texts
from summarizer import summarize_text
from memory import Memory
from query import answer_query

URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Quantum_computing",
    "https://en.wikipedia.org/wiki/Climate_change"
]


async def build_memory():
    memory = Memory("ai_memory")
    print("Fetching text content...")
    texts = await fetch_texts(URLS)

    print("Summarizing...")
    for title, text in texts.items():
        summary = await summarize_text(text)
        memory.add_document(title, summary)
        print(f"Stored: {title}")

    memory.persist()
    print("*_* Memory Updated")


async def chat_loop():
    memory = Memory("ai_memory")
    print("\nAsk Anything my child, and type exit to 'end' this\n")
    while True:
        query = input("You: ")
        if query.lower == "exit":
            break
        result = await answer_query(query, memory)
        print(f"\nAI: {result}\n")

if __name__ == "__main__":
    asyncio.run(build_memory())
    asyncio.run(chat_loop())
