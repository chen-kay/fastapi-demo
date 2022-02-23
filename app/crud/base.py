from datetime import datetime
from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from app.db.base import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)


class BaseCrud(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, session: Session, *, id: int) -> Optional[ModelType]:
        ins = (
            session.query(self.model)
            .filter(self.model.id == id, self.model.is_del == 0)
            .first()
        )
        return ins

    async def create(self, session: Session, *, model: Dict[str, Any]) -> ModelType:
        ins = self.model(**model)

        session.add(ins)
        session.commit()
        session.refresh(ins)
        return ins

    async def update(
        self,
        session: Session,
        *,
        ins: ModelType,
        model: Dict[str, Any],
    ):
        obj_data = jsonable_encoder(ins)
        update_data = model

        for field in obj_data:
            if field in update_data:
                setattr(ins, field, update_data[field])
        session.add(ins)
        session.commit()
        session.refresh(ins)
        return ins

    async def delete(
        self,
        session: Session,
        *,
        ins: ModelType,
        model: Dict[str, Any],
    ):
        obj_data = jsonable_encoder(ins)
        for field in obj_data:
            if field in model:
                setattr(ins, field, model[field])

        ins.is_del = 1
        ins.alt_at = datetime.now()
        session.add(ins)
        session.commit()
        return ins
