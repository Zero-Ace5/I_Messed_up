from datetime import datetime, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db import AsyncSessionLocal
from app.models import Price
from .fetcher import fetch_btc_price
import asyncio


async def save_price():
    async with AsyncSessionLocal() as session:
        price = await fetch_btc_price()
        if price is None:
            return
        new_entry = Price(value=price)
        session.add(new_entry)
        await session.commit()
        print(f"[{datetime.now(timezone.utc)}] BTC price recorded: ${price}")


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(save_price, "interval", seconds=10)
    scheduler.start()
