from datetime import datetime
from pydantic import BaseModel


class PriceBase(BaseModel):
    symbol: str
    value: float


class PriceCreate(PriceBase):
    pass


class PriceRead(PriceBase):
    id: int
    timestamp: datetime

    class config:
        orm_mode = True
