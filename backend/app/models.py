from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, func
from datetime import datetime
from .database import Base

class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, index=True)
    date = Column(DateTime)
    close_price = Column(Float)

class BacktestRun(Base):
    __tablename__ = "backtest_runs"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(JSON, nullable=False)
    sharpe = Column(Float, nullable=False)
    volatility = Column(Float, nullable=False)
    final_value = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
