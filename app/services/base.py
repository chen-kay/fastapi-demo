from typing import Any, Dict, Generic, TypeVar

from app.db.session import Base
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Query, Session

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    def __init__(self, model: ModelType):
        self.model = model

    def get_queryset(self, db: Session):
        return db.query(self.model)

    def pagination(self, qs: Query, *, page: int, limit: int):
        total = qs.count()
        qs = qs.offset((page - 1) * limit).limit(limit)
        return qs.all(), total

    async def create(self, db: Session, *, model: Dict[str, Any]) -> ModelType:
        ins = self.model(**model)

        db.add(ins)
        db.flush()
        return ins

    async def update(self, db: Session, *, ins: ModelType, model: Dict[str, Any]):
        obj_data = jsonable_encoder(ins)
        update_data = model

        for field in obj_data:
            if field in update_data:
                setattr(ins, field, update_data[field])
        db.add(ins)
        db.flush()
        return ins

