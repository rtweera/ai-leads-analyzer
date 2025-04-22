from fastapi import APIRouter
from app.api.v1.endpoints import ping, ingress

api_router = APIRouter()
api_router.include_router(ping.router, prefix="/ping", tags=["Ping"])
api_router.include_router(ingress.router, prefix="/leads", tags=["Leads"])