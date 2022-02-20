from app.api.api_v1.endpoints import login
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
