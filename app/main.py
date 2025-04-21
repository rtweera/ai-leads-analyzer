from fastapi import FastAPI
from app.api.v1.api import api_router
import uvicorn


app = FastAPI(title="FastAPI Template", version="0.1.0")

app.include_router(api_router, prefix="/api/v1", tags=["v1"])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="info")