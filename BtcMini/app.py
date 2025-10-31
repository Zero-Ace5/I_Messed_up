from fastapi import FastAPI
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
                "time": datetime.now(timezone.utc).isoformat(),
                "price": price
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
    return {"message": "Welcome to the BTC Price Tracker"}


@app.get('/prices')
def get_price():
    return btc_price
