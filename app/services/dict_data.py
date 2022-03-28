from typing import List, Optional, Tuple

from app import schemas
from app.models import DictData

from .base import BaseService


class DictDataService(BaseService):
    model: DictData = DictData

    async def get_list(
        self,
        *,
        company_id: int = None,
        parent_id: int,
        page: int,
        limit: int,
    ) -> Tuple[List[DictData], int]:
        """获取字典数据列表"""
        qs = (
            self.session.query(DictData)
            .filter(
                DictData.parent_id == parent_id,
                DictData.is_del == 0,
            )
            .order_by(DictData.sort)
        )
        if company_id:
            qs = qs.filter(DictData.company_id == company_id)

        total = qs.count()
        qs = qs.offset((page - 1) * limit).limit(limit)
        return qs.all(), total

    async def add(self, model: schemas.DictDataAdd):
        """新增字典数据"""
        data = model.dict(exclude_unset=True)
        return await self.create(data)

    async def edit(self, ins: DictData, *, model: schemas.DictDataEdit):
        """修改字典数据"""
        data = model.dict(exclude_unset=True)
        return await self.update(ins, model=data)

    async def get_by_id(self, id: int) -> Optional[DictData]:
        ins = (
            self.session.query(DictData)
            .filter(DictData.id == id, DictData.is_del == 0)
            .first()
        )
        return ins

    async def check_code_exists(self, code: str, *, ins: DictData = None):
        """验证编码是否存在"""
        qs = self.session.query(DictData).filter(
            DictData.code == code, DictData.is_del == 0
        )
        if ins:
            qs = qs.filter(DictData.id != ins.id)
        return self.session.query(qs.exists()).scalar()

    async def check_value_exists(self, value: str, *, ins: DictData = None):
        """验证名称是否存在"""
        qs = self.session.query(DictData).filter(
            DictData.value == value, DictData.is_del == 0
        )
        if ins:
            qs = qs.filter(DictData.id != ins.id)
        return self.session.query(qs.exists()).scalar()
