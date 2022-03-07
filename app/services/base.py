from typing import Optional

from aioredis import Redis
from app.api.db import get_redis, get_session
from fastapi import Depends
from sqlalchemy.orm import Session


class BaseService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        redis: Optional[Redis] = Depends(get_redis),
    ):
        self._session = session
        self._redis = redis
        self.initializer()

    def initializer(self):
        pass

    @property
    def session(self) -> Session:
        return self._session

    @property
    def redis(self) -> Redis:
        return self._redis
