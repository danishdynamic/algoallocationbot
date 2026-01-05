from fastapi import FastAPI, HTTPException
from app.schemas import AllocationRequest, AllocationResponse
from app.assetbot import Backtest
from fastapi.middleware.cors import CORSMiddleware # to add frontend for cors

app = FastAPI( title="Asset Allocation Bot API")

#@app.get("/health")
#def health_check():
   # return {"status": "ok"}

#Open in browser fast api server: API docs → http://127.0.0.1:8000/docs  Health check → http://127.0.0.1:8000/health

from fastapi import HTTPException

@app.post("/allocate")
async def allocate(req: AllocationRequest):
    if not req.tickers:
        raise HTTPException(status_code=400, detail="No tickers provided")

    try:
        # Create one instance of the backtester
        bt = Backtest(
            symbol=req.tickers[0], 
            initial_money=req.capital
        )
        
        # Run the simulation and return the dict
        result = bt.run()
        return result

    except Exception as e:
        # This captures data loading errors (like invalid tickers)
        raise HTTPException(status_code=500, detail=str(e))
    

# to add frontend for cors 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

