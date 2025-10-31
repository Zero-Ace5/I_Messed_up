from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import httpx
import asyncio
from datetime import datetime, timezone

btc_price = []


async def fetch_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        data = response.json()
        return data["bitcoin"]["usd"]


async def record_price():
    while True:
        try:
            price = await fetch_price()
            btc_price.append({
                "time": datetime.now(timezone.utc).strftime(("%Y-%m-%d %H:%M:%S UTC")),
                "price": round(price, 2)
            })
            print(f"[{datetime.now(timezone.utc)}] BTC: ${price}")
        except Exception as e:
            print(f"Error fetching price. Coingecko API failed me: {e}")
        await asyncio.sleep(10)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(record_price())
    yield
    task.cancel()

app = FastAPI(title="Mini Btc App", lifespan=lifespan)


@app.get('/')
def root():
    return {"message": "Welcome to the BTC Price Tracker. Visit /prices or /prices/html"}


@app.get('/prices')
def get_price():
    return {
        "count": len(btc_price),
        "latest": btc_price[-1] if btc_price else None,
        "history": btc_price
    }


@app.get("/prices/html", response_class=HTMLResponse)
def get_prices_html():
    """Returns price data in a simple HTML table."""
    html = """
    <html>
    <head>
        <title>BTC Price Tracker</title>
        <style>
            body { font-family: Arial; padding: 20px; background-color: #f8f9fa; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 60%; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: center; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Bitcoin Prices (USD)</h1>
        <table>
            <tr><th>Time</th><th>Price (USD)</th></tr>
    """
    for entry in reversed(btc_price[-20:]):  # show last 20 entries
        html += f"<tr><td>{entry['time']}</td><td>${entry['price']}</td></tr>"
    html += "</table></body></html>"
    return HTMLResponse(content=html)


# To run  uvicorn app:app --reload
