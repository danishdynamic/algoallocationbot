from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class PricePoint(BaseModel):
    date: str
    price: float


class BacktestResult(BaseModel):
    symbol: str
    initial_money: float
    sharpe: float
    volatility: float
    final_account_value: float
    transactions: Dict[str, List[Any]]
    history: List[PricePoint]   #charts


class AllocationResponse(BaseModel):
    results: Dict[str, BacktestResult]
    error: Optional[Dict[str, str]] = None

    """   symbol: str  #for single asset we only use allocation response and not calss backtest resullt
    initial_money: float
    sharpe: float
    volatility: float
    final_account_value: float
    transactions: Dict[str, List[Any]]"""


class AllocationRequest(BaseModel):
    tickers: List[str]
    capital: float




