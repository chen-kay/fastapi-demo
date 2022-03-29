import json
from typing import List, Tuple

from app import schemas
from app.models import Company

from .base import BaseCrud


class CrudCompany(BaseCrud["Company"]):
    model = Company

    async def get_list(
        self,
        *,
        page: int,
        limit: int,
    ) -> Tuple[List[Company], int]:
        """获取企业列表"""
        qs = (
            self.session.query(Company)
            .filter(Company.is_del == 0)
            .order_by(Company.sort)
        )

        total = qs.count()
        qs = qs.offset((page - 1) * limit).limit(limit)
        return qs.all(), total

    async def find_by_id(self, id: int) -> schemas.CompanyModel:
        """从缓存获取企业 - 企业id"""
        key = f"enterp:id:{id}"
        if self.redis and await self.redis.exists(key):
            user_str = await self.redis.get(key)
            user_dict = json.loads(user_str)
            model = schemas.CompanyModel(**user_dict)
        else:
            ins = await self.get_by_id(id)
            model = schemas.CompanyModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(model.dict(), ensure_ascii=False)
            )
        return model

    async def check_code_exists(self, code: str, *, ins: Company = None):
        """验证编码是否存在"""
        qs = self.session.query(Company).filter(
            Company.code == code, Company.is_del == 0
        )
        if ins:
            qs = qs.filter(Company.id != ins.id)
        return self.session.query(qs.exists()).scalar()

    async def check_name_exists(self, name: str, *, ins: Company = None):
        """验证名称是否存在"""
        qs = self.session.query(Company).filter(
            Company.name == name, Company.is_del == 0
        )
        if ins:
            qs = qs.filter(Company.id != ins.id)
        return self.session.query(qs.exists()).scalar()
