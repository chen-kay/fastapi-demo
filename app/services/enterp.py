"""Enterp Services module."""

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
    def initializer(self):
        self.enterp = crud.Enterp(self.session, self.redis)

    async def get_enterp_list(self, model: EnterpFilter):
        return await self.enterp.get_enterp_list(
            keyword=model.keyword,
            is_active=model.is_active,
            page=model.page,
            page_size=model.page_size,
        )

    async def create(self, *, model: EnterpCreate, current: UserModel):
        """创建企业"""
        create_data = model.dict(exclude_unset=True)
        create_data["add_user_id"] = current.id
        create_data["alt_user_id"] = current.id

        ins = await self.enterp.create(create_data)
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

        ins = await crud.enterp.update(ins, model=update_data)
        await self.enterp.clear_cache(ins)
        return ins

    async def delete(self, ins: Enterp, *, current: UserModel):
        """删除企业"""
        update_data = dict(del_user_id=current.id)
        ins = await self.enterp.delete(ins, model=update_data)
        await self.enterp.clear_cache(ins)
        return ins

    async def get_by_domain(self, domain: str):
        return await self.enterp.get_by_domain(domain)

    async def get_by_id(self, id: int):
        return await self.enterp.get_by_id(id)

    async def find_by_domain(self, domain: str):
        return await self.enterp.find_by_domain(domain)

    async def find_by_id(self, id: int):
        return await self.enterp.find_by_id(id)

    async def is_active(self, user: Union[Enterp, EnterpModel]) -> bool:
        """是否可用"""
        return user.is_active
