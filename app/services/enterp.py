"""Enterp Services module."""

import json
from datetime import datetime
from typing import Union

from app import crud
from app.models import Enterp
from app.schemas.models.enterp import (
    EnterpCreate,
    EnterpFilter,
    EnterpModel,
    EnterpUpdate,
)
from app.schemas.models.user import UserModel

from .base import BaseService


class EnterpService(BaseService):
    async def get_enterp_list(self, model: EnterpFilter):
        return await crud.enterp.get_enterp_list(
            self.session,
            keyword=model.keyword,
            page=model.page,
            page_size=model.page_size,
        )

    async def create(self, *, model: EnterpCreate, current: UserModel):
        """创建企业"""
        create_data = model.dict(exclude_unset=True)
        create_data["add_user_id"] = current.id
        create_data["alt_user_id"] = current.id

        ins = await crud.enterp.create(self.session, model=create_data)
        return ins

    async def update(
        self,
        ins: Enterp,
        *,
        model: EnterpUpdate,
        current: UserModel,
    ):
        """修改企业"""
        update_data = model.dict(exclude_unset=True)
        update_data["alt_user_id"] = current.id

        ins = await crud.enterp.update(self.session, ins=ins, model=update_data)
        await self.clear_cache(ins)
        return ins

    async def delete(self, ins: Enterp, *, current: UserModel):
        """删除企业"""
        update_data = dict(del_user_id=current.id)
        ins = await crud.enterp.delete(self.session, ins=ins, model=update_data)
        await self.clear_cache(ins)
        return ins

    async def get_by_domain(self, domain: str):
        return await crud.enterp.get_by_domain(self.session, domain=domain)

    async def get_by_id(self, id: int):
        return await crud.enterp.get_by_id(self.session, id=id)

    async def find_by_id(self, id: int):
        key = f"enterp:id:{id}"
        if self.redis and await self.redis.exists(key):
            enterp_str = await self.redis.get(key)
            enterp_dict = json.loads(enterp_str)
            model = EnterpModel(**enterp_dict)
        else:
            ins = await self.get_by_id(id)
            model = EnterpModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(model.dict(exclude_unset=True), ensure_ascii=False)
            )
        return model

    async def find_by_domain(self, domain: str):
        key = f"enterp:domain:{domain}"
        if self.redis and await self.redis.exists(key):
            enterp_str = await self.redis.get(key)
            enterp_dict = json.loads(enterp_str)
            model = EnterpModel(**enterp_dict)
        else:
            ins = await self.get_by_domain(domain)
            model = EnterpModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(model.dict(exclude_unset=True), ensure_ascii=False)
            )
        return model

    async def is_active(self, user: Union[Enterp, EnterpModel]) -> bool:
        """是否可用"""
        return user.is_active

    async def clear_cache(self, ins: Enterp):
        """清除缓存"""
        if not self.redis:
            return
        self.redis.delete(f"enterp:id:{ins.id}")
        self.redis.delete(f"enterp:domain:{ins.domain}")
