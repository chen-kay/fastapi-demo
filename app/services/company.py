import json
from typing import List, Optional, Tuple

from app import schemas
from app.models import Company

from .base import BaseService


class CompanyService(BaseService["Company"]):
    model = Company

    async def get_list(
        self,
        *,
        page: int = None,
        limit: int = None,
    ) -> Tuple[List[Company], int]:
        """获取企业列表"""
        qs = (
            self.session.query(Company)
            .filter(Company.is_del == 0)
            .order_by(Company.sort)
        )
        return self.pagination(qs, page, limit)

    async def add(self, model: schemas.CompanyAdd):
        """新增企业"""
        return await self.create(model.dict())

    async def edit(self, ins: Company, *, model: schemas.CompanyEdit):
        """修改企业"""
        return await self.update(ins, model=model.dict(exclude_unset=True))

    async def get_by_id(self, id: int) -> Optional[Company]:
        """从数据库获取企业 - 企业id"""
        qs = self.session.query(Company).filter(
            Company.is_del == 0,
            Company.id == id,
        )
        ins = qs.first()
        return ins

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

    def is_active(self, ins: Company) -> bool:
        """企业是否可用"""
        return ins.is_del == 0 and ins.status == 1

    async def check_domain_exists(self, domain: str, *, ins: Company = None):
        """验证编码是否存在"""
        qs = self.session.query(Company).filter(
            Company.domain == domain, Company.is_del == 0
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
