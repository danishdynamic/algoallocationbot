from pydantic import BaseModel
from typing import Dict, List

class AllocationRequest(BaseModel):
    tickers: List[str]
    capital: float

class AllocationResponse(BaseModel):
    allocation: Dict[str, float]