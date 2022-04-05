from typing import Optional

from app import schemas
from app.models import DictData
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from .base import BaseService


class DictDataService(BaseService["DictData"]):
    async def get_list(
        self,
        db: Session,
        *,
        company_id: int = None,
        parent_id: int = None,
        keyword: str = None,
    ):
        qs = self.get_queryset(db).filter(
            DictData.is_del == 0,
            DictData.company_id == company_id,
            DictData.parent_id == parent_id,
        )
        if keyword:
            qs = qs.filter(
                or_(
                    DictData.value.like(f"%{keyword}%"),
                    DictData.code.like(f"%{keyword}%"),
                )
            )
        return qs

    async def add(
        self,
        db: Session,
        *,
        model: schemas.DictDataAdd,
        company_id: int,
    ):
        """新增字典值"""
        ins = await self.create(
            db,
            model=dict(
                **model.dict(),
                company_id=company_id,
            ),
        )
        return ins

    async def edit(
        self,
        db: Session,
        *,
        ins: DictData,
        model: schemas.DictDataEdit,
    ):
        """修改字典值"""
        ins = await self.update(db, ins=ins, model=model.dict(exclude_unset=True))
        return ins

    async def delete(self, db: Session, *, ins: DictData):
        """删除字典值"""
        ins = await self.update(db, ins=ins, model=dict(is_del=1))
        return ins

    async def get_by_id(
        self,
        db: Session,
        *,
        id: int,
        company_id: int,
    ) -> Optional[DictData]:
        """从数据库获取字典值 - 字典值id"""
        qs = db.query(DictData).filter(
            DictData.is_del == 0,
            DictData.company_id == company_id,
            DictData.id == id,
        )
        ins = qs.first()
        return ins

    async def check_code_exists(
        self,
        db: Session,
        *,
        code: str,
        company_id: int,
        ins: DictData = None,
    ):
        """验证编码是否存在"""
        qs = db.query(DictData).filter(
            DictData.code == code,
            DictData.company_id == company_id,
            DictData.is_del == 0,
        )
        if ins:
            qs = qs.filter(DictData.id != ins.id)
        return qs.exists()

    async def check_value_exists(
        self,
        db: Session,
        *,
        value: str,
        company_id: int,
        ins: DictData = None,
    ):
        """验证字典值是否存在"""
        qs = db.query(DictData).filter(
            DictData.value == value,
            DictData.company_id == company_id,
            DictData.is_del == 0,
        )
        if ins:
            qs = qs.filter(DictData.id != ins.id)
        return qs.exists()


dict_data = DictDataService(DictData)
