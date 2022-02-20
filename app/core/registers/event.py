"""连接初始化
"""
from typing import Optional

from aioredis import Redis
from app.db.redis import get_redis_pool
from fastapi import FastAPI


def register_event(app: FastAPI) -> None:
    @app.on_event("startup")
    async def startup_event():
        app.state.redis = await get_redis_pool()

    @app.on_event("shutdown")
    async def shutdown_event():
        redis: Optional[Redis] = app.state.redis
        if redis:
            await redis.close()
