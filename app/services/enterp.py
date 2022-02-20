"""User Services module."""

import json
from typing import Union

from app.models import Enterp
from app.schemas.models.enterp import EnterpModel

from .base import BaseService


class EnterpService(BaseService):
    async def get_by_id(self, id: int):
        enterp = (
            self.session.query(Enterp)
            .filter(Enterp.id == id, Enterp.is_del == 0)
            .first()
        )
        return enterp

    async def find_by_id(self, id: int):
        key = f"enterp:enterp_id:{id}"
        if self.redis and await self.redis.exists(key):
            enterp_str = await self.redis.get(key)
            enterp_dict = json.loads(enterp_str)
            enterp = EnterpModel(**enterp_dict)
        else:
            ins = await self.get_by_id(id=id)
            enterp = EnterpModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(enterp.dict(), ensure_ascii=False)
            )
        return enterp

    async def is_active(self, user: Union[Enterp, EnterpModel]) -> bool:
        """是否可用"""
        return user.is_active
