from fastapi import FastAPI
from contextlib import asynccontextmanager
from .db import Base, engine
from .routes import prices
from .services.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("[Init] Scheduler starting...")
    start_scheduler()
    print("Fetching BTC price...")
    yield  # app runs here
    print("[Shutdown] App stopped.")


app = FastAPI(title="Async Bitcoin Tracker", lifespan=lifespan)

app.include_router(prices.router)
