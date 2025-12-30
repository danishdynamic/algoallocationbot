from fastapi import FastAPI, HTTPException
from app.schemas import AllocationRequest, AllocationResponse
from app.assetbot import Backtest

app = FastAPI( title="Asset Allocation Bot API")

#@app.get("/health")
#def health_check():
   # return {"status": "ok"}

#Open in browser fast api server: API docs → http://127.0.0.1:8000/docs  Health check → http://127.0.0.1:8000/health

@app.post("/allocate", response_model=AllocationResponse)
def allocate(req: AllocationRequest):
    try:
        bt = Backtest(
            symbol=req.ticker,
            initial_money=req.capital
        )
        result = bt.run()
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))