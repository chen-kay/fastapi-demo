"""注册路由
"""
from app.api.api_v1 import api
from fastapi import FastAPI


def register_router(app: FastAPI) -> None:
    """注册路由"""
    app.include_router(api.api_router)
