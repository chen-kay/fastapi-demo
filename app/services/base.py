from typing import Any, Dict, Generic, Optional, Type, TypeVar

from aioredis import Redis
from app.api.deps import get_redis, get_session
from app.db.base import Base
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

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

    async def create(self, model: Dict[str, Any]) -> ModelType:
        ins = self.model(**model)

        self.session.add(ins)
        self.session.flush()
        print(ins)
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

    async def delete(
        self,
        ins: ModelType,
        *,
        model: Dict[str, Any] = {},
    ):
        obj_data = jsonable_encoder(ins)
        for field in obj_data:
            if field in model:
                setattr(ins, field, model[field])

        ins.is_del = 1
        self.session.add(ins)
        self.session.flush()
        return ins

    def __del__(self):
        self.session.commit()
