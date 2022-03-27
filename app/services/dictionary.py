from typing import List, Tuple

from app.models import Dictionary, DictValue

from .base import BaseService


class DictService(BaseService):
    async def get_dictionary_list(self) -> List[Dictionary]:
        """获取数据字典列表"""
        qs = self.session.query(Dictionary).filter(Dictionary.status == 1)
        return qs.all()

    async def get_dictvalue_list(
        self,
        *,
        company_id: int = None,
        parent_id: int,
        page: int,
        limit: int,
    ) -> Tuple[List[Dictionary], int]:
        """获取字典值列表"""
        qs = self.session.query(DictValue).filter(
            DictValue.parent_id == parent_id,
            DictValue.is_del == 0,
        )
        if company_id:
            qs = qs.filter(DictValue.company_id == company_id)

        total = qs.count()
        qs = qs.offset((page - 1) * limit).limit(limit)
        return qs.all(), total
