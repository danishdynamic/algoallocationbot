from fastapi import FastAPI

app = FastAPI(
    title="Asset Allocation Bot API",
    description="API for the Asset Allocation Bot application",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}



#Open in browser fast api server:

#API docs → http://127.0.0.1:8000/docs

#Health check → http://127.0.0.1:8000/health

     