import json
from typing import Optional

from aioredis import Redis
from app.models import User
from app.schemas.models.user import UserModel
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from .base import BaseCrud


class UserCrud(BaseCrud[User]):
    model = User

    async def get_user_list(
        self,
        *,
        keyword: str,
        page: int,
        page_size: int,
    ):
        qs = self.session.query(User).filter(User.is_del == 0)
        if keyword:
            qs = qs.filter(
                or_(
                    User.fullname.like(f"%{keyword}%"),
                    User.username.like(f"%{keyword}%"),
                )
            )

        total = qs.count()
        qs = qs.offset((page - 1) * page_size).limit(page_size).all()
        return qs, total

    async def get_by_user_name(self, user_name: str):
        qs = self.session.query(User).filter(
            User.is_del == 0,
            User.user_name == user_name,
        )
        ins = qs.first()
        return ins

    async def get_by_id(self, id: int):
        qs = self.session.query(User).filter(
            User.is_del == 0,
            User.id == id,
        )
        ins = qs.first()
        return ins

    async def find_by_user_name(self, user_name: str):
        key = f"user:user_name:{user_name}"
        if self.redis and await self.redis.exists(key):
            user_str = await self.redis.get(key)
            user_dict = json.loads(user_str)
            user = UserModel(**user_dict)
        else:
            ins = await self.get_by_user_name(user_name)
            user = UserModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(user.dict(), ensure_ascii=False)
            )
        return user

    async def find_by_id(self, id: int):
        key = f"user:user_id:{id}"
        if self.redis and await self.redis.exists(key):
            user_str = await self.redis.get(key)
            user_dict = json.loads(user_str)
            user = UserModel(**user_dict)
        else:
            ins = await self.get_by_id(id)
            user = UserModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(user.dict(), ensure_ascii=False)
            )
        return user
