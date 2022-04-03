from typing import Generator, Optional

from aioredis import Redis
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from starlette.requests import Request


def get_session() -> Generator:
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise e
    finally:
        db.close()


async def get_redis(request: Request) -> Optional[Redis]:
    redis = request.app.state.redis
    if not isinstance(redis, Redis):
        return None
    return redis
