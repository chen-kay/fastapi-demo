"""Enterp Services module."""

from datetime import datetime
from typing import Literal

from app import crud
from app.models import Enterp
from app.schemas.models.enterp import EnterpCreate, EnterpUpdate
from app.schemas.models.user import UserModel

from .base import BaseService


class EnterpService(BaseService):
    def initializer(self):
        self.enterp = crud.Enterp(self.session, self.redis)

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
        if ins.is_active == 3 and (
            not model.expire_at or model.expire_at > datetime.now()
        ):
            # 账号过期时修改过期时间后变更企业状态
            update_data["is_active"] = 1

        ins = await self.enterp.update(ins, model=update_data)
        await self.enterp.clear_cache(ins)
        return ins

    async def update_status(
        self,
        ins: Enterp,
        *,
        is_active: Literal[1, 2],
        current: UserModel,
    ):
        """修改企业状态"""
        update_data = dict(is_active=is_active)
        update_data["alt_user_id"] = current.id
        ins = await self.enterp.update(ins, model=update_data)

        if is_active:
            # Todo. 企业禁用后操作
            pass
        return ins

    async def delete(self, ins: Enterp, *, current: UserModel):
        """删除企业"""
        update_data = dict(del_user_id=current.id)
        ins = await self.enterp.delete(ins, model=update_data)
        await self.enterp.clear_cache(ins)
        # Todo. 企业删除后操作
        return ins
