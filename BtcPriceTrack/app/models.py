from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, String
from .db import Base


class Price(Base):
    __tablename__ = "prices"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, default="BTC")
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
