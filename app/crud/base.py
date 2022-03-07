from typing import Any, Dict, Generic, Optional, Type, TypeVar

from aioredis import Redis
from app.db.base import Base
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)


class BaseCrud(Generic[ModelType]):
    model: Type[ModelType]

    def __init__(self, session: Session, redis: Optional[Redis] = None):
        self.session = session
        self.redis = redis

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        ins = (
            self.session.query(self.model)
            .filter(self.model.id == id, self.model.is_del == 0)
            .first()
        )
        return ins

    async def create(self, model: Dict[str, Any]) -> ModelType:
        ins = self.model(**model)

        self.session.add(ins)
        self.session.commit()
        self.session.refresh(ins)
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
        self.session.commit()
        self.session.refresh(ins)
        return ins

    async def delete(
        self,
        ins: ModelType,
        *,
        model: Dict[str, Any],
    ):
        obj_data = jsonable_encoder(ins)
        for field in obj_data:
            if field in model:
                setattr(ins, field, model[field])

        ins.is_del = 1
        self.session.add(ins)
        self.session.commit()
        return ins
