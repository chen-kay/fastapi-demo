import json
from typing import Optional, Union

from app import schemas
from app.core.security import get_password_hash, verify_password
from app.models import Company, User

from .base import BaseService


class UserService(BaseService["User"]):
    model: User = User

    async def create_admin_user(self, ins: Company):
        model = dict(
            company_id=ins.id,
            username="admin",
            fullname="admin",
            nickname="系统管理员",
            hashed_password=get_password_hash("123456"),
            is_admin=1,
        )
        ins = await self.create(model)
        return ins

    async def get_by_id(self, id: int) -> Optional[User]:
        """从数据库获取用户 - 用户id"""
        qs = self.session.query(User).filter(
            User.is_del == 0,
            User.id == id,
        )
        ins = qs.first()
        return ins

    async def find_by_id(self, id: int) -> schemas.UserModel:
        """从缓存获取用户 - 用户id"""
        key = f"user:id:{id}"
        if self.redis and await self.redis.exists(key):
            user_str = await self.redis.get(key)
            user_dict = json.loads(user_str)
            model = schemas.UserModel(**user_dict)
        else:
            ins = await self.get_by_id(id)
            model = schemas.UserModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(model.dict(), ensure_ascii=False)
            )
        return model

    async def get_by_username(self, username: str) -> Optional[User]:
        """从数据库获取用户 - 用户名"""
        qs = self.session.query(User).filter(
            User.is_del == 0,
            User.username == username,
        )
        ins = qs.first()
        return ins

    async def find_by_username(self, username: str) -> schemas.UserModel:
        """从缓存获取用户 - 用户名"""
        key = f"user:username:{username}"
        if self.redis and await self.redis.exists(key):
            user_str = await self.redis.get(key)
            user_dict = json.loads(user_str)
            user = schemas.UserModel(**user_dict)
        else:
            ins = await self.get_by_username(username)
            user = schemas.UserModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(user.dict(), ensure_ascii=False)
            )
        return user

    async def authenticate(self, *, username: str, password: str) -> User:
        """用户认证"""
        user = await self.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: Union[User, schemas.UserModel]) -> bool:
        """用户是否可用"""
        if not user:
            return False
        return user.status == 1

    def is_superuser(self, user: Union[User, schemas.UserModel]) -> bool:
        """用户是否超级管理员"""
        return user.is_superuser
