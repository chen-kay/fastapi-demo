from typing import Optional

from app.models import DictType
from sqlalchemy.orm import Session

from .base import BaseService


class DictTypeService(BaseService["DictType"]):
    async def get_list(self, db: Session):
        qs = self.get_queryset(db).filter(DictType.status == 1, DictType.is_del == 0)
        return qs.all()

    async def get_by_id(self, db: Session, *, id: int) -> Optional[DictType]:
        """从数据库获取字典 - 字典id"""
        qs = db.query(DictType).filter(
            DictType.is_del == 0,
            DictType.id == id,
        )
        ins = qs.first()
        return ins


dict_type = DictTypeService(DictType)
