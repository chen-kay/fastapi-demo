import json
from datetime import date
from typing import List

from app.models import Enterp, User
from app.schemas.models.enterp import EnterpModel
from sqlalchemy.sql import or_

from .base import BaseCrud


class EnterpCrud(BaseCrud[Enterp]):
    model = Enterp

    async def get_enterp_list(
        self,
        *,
        domain: str = "",
        name: str = "",
        short_name: str = "",
        expire_at: List[date] = [],
        is_active: int = None,
        keyword: str = "",
        page: int,
        page_size: int,
    ):
        qs = self.session.query(Enterp).filter(Enterp.is_del == 0)
        if domain:
            qs = qs.filter(Enterp.domain.like(f"%{domain}%"))
        if name:
            qs = qs.filter(Enterp.name.like(f"%{name}%"))
        if short_name:
            qs = qs.filter(Enterp.short_name.like(f"%{short_name}%"))
        if expire_at:
            qs = qs.filter(Enterp.expire_at.between(expire_at[0], expire_at[1]))
        if is_active:
            qs = qs.filter(Enterp.is_active == is_active)
        if keyword:
            qs = qs.filter(
                or_(
                    Enterp.domain.like(f"%{keyword}%"),
                    Enterp.name.like(f"%{keyword}%"),
                    Enterp.short_name.like(f"%{keyword}%"),
                )
            )

        total = qs.count()
        qs = qs.offset((page - 1) * page_size).limit(page_size).all()
        return qs, total

    async def get_by_domain(self, domain: str):
        ins = (
            self.session.query(Enterp)
            .filter(Enterp.domain == domain, Enterp.is_del == 0)
            .first()
        )
        return ins

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

    async def clear_cache(self, ins: Enterp):
        """清除缓存"""
        if not self.redis:
            return
        self.redis.delete(f"enterp:id:{ins.id}")
        self.redis.delete(f"enterp:domain:{ins.domain}")
