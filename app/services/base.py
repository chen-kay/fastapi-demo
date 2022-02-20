from typing import Optional

from aioredis import Redis
from sqlalchemy.orm import Session


class BaseService:
    def __init__(self, session: Session, redis: Optional[Redis] = None) -> None:
        self._session = session
        self._redis = redis

    @property
    def session(self) -> Session:
        return self._session

    @property
    def redis(self) -> Redis:
        return self._redis
