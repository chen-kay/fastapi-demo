"""Enterp Services module."""

import json
from datetime import datetime
from typing import Union

from app.models import Enterp
from app.schemas.models.enterp import (
    EnterpCreate,
    EnterpFilter,
    EnterpModel,
    EnterpUpdate,
)
from app.schemas.models.user import UserModel
from fastapi.encoders import jsonable_encoder
from sqlalchemy.sql import or_

from .base import BaseService


class EnterpService(BaseService):
    async def get_enterp_list(self, filter: EnterpFilter):
        qs = self.session.query(Enterp).filter(Enterp.is_del == 0)
        if filter.keyword:
            qs = qs.filter(
                or_(
                    Enterp.domain.like(f"%{filter.keyword}%"),
                    Enterp.name.like(f"%{filter.keyword}%"),
                    Enterp.short_name.like(f"%{filter.keyword}%"),
                )
            )

        total = qs.count()
        qs = (
            qs.offset((filter.page - 1) * filter.page_size)
            .limit(filter.page_size)
            .all()
        )
        return qs, total

    async def get_by_domain(self, domain: str):
        enterp = (
            self.session.query(Enterp)
            .filter(Enterp.domain == domain, Enterp.is_del == 0)
            .first()
        )
        return enterp

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
                key, json.dumps(enterp.dict(exclude_unset=True), ensure_ascii=False)
            )
        return enterp

    async def is_active(self, user: Union[Enterp, EnterpModel]) -> bool:
        """是否可用"""
        return user.is_active

    async def create(self, *, model: EnterpCreate, current: UserModel):
        """创建企业"""
        ins = Enterp(**model.dict(exclude_unset=True))
        ins.alt_user_id = current.id
        ins.add_user_id = current.id

        self.session.add(ins)
        self.session.commit()
        self.session.refresh(ins)
        return ins

    async def update(
        self,
        ins: Enterp,
        *,
        model: EnterpUpdate,
        current: UserModel,
    ):
        """修改企业"""
        obj_data = jsonable_encoder(ins)
        update_data = model.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(ins, field, update_data[field])

        ins.alt_user_id = current.id

        self.session.add(ins)
        self.session.commit()
        self.session.refresh(ins)
        return ins

    async def delete(self, ins: Enterp, current: UserModel = None):
        """删除企业"""
        # if current:
        #     ins.del_user_id = current.id
        ins.domain = f"{ins.id}_{ins.domain}"
        ins.is_del = 1
        ins.alt_at = datetime.now()
        self.session.add(ins)
        self.session.commit()
        self.session.refresh(ins)
        return ins
