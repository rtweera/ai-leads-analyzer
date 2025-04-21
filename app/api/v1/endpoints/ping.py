from fastapi import APIRouter
from app.schemas.ping import PingResponse

router = APIRouter()

@router.get("/", response_model=PingResponse, tags=["Ping"])
async def ping():
    return {"message": "pong"}