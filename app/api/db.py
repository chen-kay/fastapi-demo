from typing import Callable, Generator, Optional, Type

from aioredis import Redis
from app.db.session import SessionLocal
from app.services.base import BaseService
from fastapi import Depends
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


def get_services(
    serv_type: Type[BaseService],
) -> Callable[[Session], BaseService]:
    def _get_repo(
        session: Session = Depends(get_session),
        redis: Redis = Depends(get_redis),
    ) -> BaseService:
        return serv_type(session=session, redis=redis)

    return _get_repo
