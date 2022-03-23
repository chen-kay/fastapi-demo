"""跨域设置"""
from app.core.config import settings
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def register_cors(app: FastAPI) -> None:
    if settings.DEBUG:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
