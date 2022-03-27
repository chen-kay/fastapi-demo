from typing import Generator, Optional

from aioredis import Redis
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from starlette.requests import Request


async def get_redis(request: Request) -> Optional[Redis]:
    redis = request.app.state.redis
    if not isinstance(redis, Redis):
        return None
    return redis


def get_session() -> Generator:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()