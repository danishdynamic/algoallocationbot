from fastapi import FastAPI, HTTPException , Request , Depends
from .schemas import AllocationRequest, AllocationResponse
from .assetbot import Backtest, save_backtest_run
from fastapi.middleware.cors import CORSMiddleware # to add frontend for cors
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from .models import Base
from contextlib import asynccontextmanager
from .database import engine
from sqlalchemy.orm import Session
from .database import get_db

# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: any cleanup can be done here
app = FastAPI(lifespan=lifespan, title="Asset Allocation Bot API")

#@app.get("/health")
#def health_check():
# return {"status": "ok"}

#Open in browser fast api server: API docs → http://127.0.0.1:8000/docs  Health check → http://127.0.0.1:8000/health

#add handler for rate limit exceeded
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


from fastapi import HTTPException

@app.post("/allocate", response_model=AllocationResponse)
@limiter.limit("10/minute")  # Limit to 10 requests per minute per IP
async def allocate(request: Request, req: AllocationRequest, db: Session = Depends(get_db)) -> AllocationResponse:
    if not req.tickers:
        raise HTTPException(status_code=400, detail="No tickers provided")
    
    results = {}

    capital_per_asset = req.capital / len(req.tickers)

    for ticker in req.tickers:
        try:
            bt = Backtest(symbol=ticker, initial_money=capital_per_asset)
            result = bt.run()
            # Save the backtest run to the database
            save_backtest_run(db, result)
            results[ticker] = result
        except Exception as e:
           print(f"Error on {ticker}: {e}")
           raise HTTPException(status_code=500, detail=f"Error processing ticker {ticker}: {str(e)}")
        
    return {"ticker": ", ".join(req.tickers),"results": results, "error": None}

"""    try:
        # Create one instance of the backtester
        bt = Backtest(
            symbol=req.tickers[0], 
            initial_money=req.capital
        )                                # single asset 
        
        # Run the simulation and return the dict
        result = bt.run()
        # Save the backtest run to the database
        save_backtest_run(db, result)
        return result

    except Exception as e:
        # This captures data loading errors (like invalid tickers)
        raise HTTPException(status_code=500, detail=str(e)) """
    
# this overrides the default rate limit message rather plain text
def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Rate limit exceeded. Please try again later."},
    )

    

# to add frontend for cors 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust this to your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

