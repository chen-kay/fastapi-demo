from typing import List, Optional

from app.models import DictType

from .base import BaseCrud


class CrudDictType(BaseCrud["DictType"]):
    model: DictType = DictType

    async def get_list(self) -> List[DictType]:
        """获取数据字典列表"""
        qs = self.session.query(DictType).filter(DictType.status == 1)
        return qs.all()

    async def get_by_id(self, id: int) -> Optional[DictType]:
        ins = (
            self.session.query(DictType)
            .filter(DictType.id == id, DictType.is_del == 0)
            .first()
        )
        return ins

    async def check_code_exists(self, code: str, *, ins: DictType = None):
        """验证编码是否存在"""
        qs = self.session.query(DictType).filter(
            DictType.code == code, DictType.is_del == 0
        )
        if ins:
            qs = qs.filter(DictType.id != ins.id)
        return qs.exists()

    async def check_name_exists(self, name: str, *, ins: DictType = None):
        """验证名称是否存在"""
        qs = self.session.query(DictType).filter(
            DictType.name == name, DictType.is_del == 0
        )
        if ins:
            qs = qs.filter(DictType.id != ins.id)
        return qs.exists()
