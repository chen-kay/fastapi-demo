import json
from typing import Optional

from app import schemas
from app.models import Company

from .base import BaseService


class CompanyService(BaseService):
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
