import httpx
from bs4 import BeautifulSoup


async def fetch_texts(urls: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0 Safari/537.36"
        )
    }

    texts = {}
    async with httpx.AsyncClient(timeout=30, headers=headers) as client:
        for url in urls:
            res = await client.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            title = soup.title.string if soup.title else url
            text = " ".join([p.get_text() for p in soup.find_all("p")])
            texts[title] = text
    return texts
