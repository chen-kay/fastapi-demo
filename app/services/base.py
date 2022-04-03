from typing import Any, Dict, Generic, Optional, Type, TypeVar

from aioredis import Redis
from app.db.deps import get_redis, get_session
from app.db.session import Base
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Query, Session

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(
        self,
        session: Session = Depends(get_session),
        redis: Optional[Redis] = Depends(get_redis),
    ):
        self._session = session
        self._redis = redis

    @property
    def session(self) -> Session:
        return self._session

    @property
    def redis(self) -> Redis:
        return self._redis

    def pagination(
        self,
        qs: Query,
        page: int,
        limit: int,
    ):
        total = qs.count()
        qs = qs.offset((page - 1) * limit).limit(limit)
        return qs.all(), total

    async def create(self, model: Dict[str, Any]) -> ModelType:
        ins = self.model(**model)

        self.session.add(ins)
        self.session.flush()
        return ins

    async def update(
        self,
        ins: ModelType,
        *,
        model: Dict[str, Any],
    ):
        obj_data = jsonable_encoder(ins)
        update_data = model

        for field in obj_data:
            if field in update_data:
                setattr(ins, field, update_data[field])
        self.session.add(ins)
        self.session.flush()
        return ins
