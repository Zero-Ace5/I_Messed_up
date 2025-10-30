from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..db import get_db
from ..models import Price
from ..schemas import PriceRead
from typing import List

router = APIRouter(prefix="/api/prices", tags=["Prices"])


@router.get("/", response_model=List[PriceRead])
async def get_prices(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Price).order_by(Price.timestamp.desc()).limit(10))
    return result.scalars().all()
