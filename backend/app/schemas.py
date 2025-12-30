from pydantic import BaseModel
from typing import Dict, List, Any

class AllocationRequest(BaseModel):
    tickers: List[str]
    capital: float

class AllocationResponse(BaseModel):
    symbol: str
    initial_money: float
    sharpe: float
    volatility: float
    final_account_value: float
    transactions: Dict[str, List[Any]]
