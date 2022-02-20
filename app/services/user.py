"""User Services module."""

import json
from typing import Optional, Union

from app.core.security import verify_password
from app.models.user import User
from app.schemas.models.user import UserModel

from .base import BaseService


class UserService(BaseService):
    async def get_by_user_name(self, user_name: str):
        user = (
            self.session.query(User)
            .filter(User.user_name == user_name, User.is_del == 0)
            .first()
        )
        return user

    async def find_by_user_name(self, user_name: str):
        key = f"user:user_name:{user_name}"
        if self.redis and await self.redis.exists(key):
            user_str = await self.redis.get(key)
            user_dict = json.loads(user_str)
            user = UserModel(**user_dict)
        else:
            ins = await self.get_by_user_name(user_name=user_name)
            user = UserModel.from_orm(ins)
            await self.redis.set(key, json.dumps(user.dict(), ensure_ascii=False))
        return user

    async def authenticate(self, user_name: str, password: str) -> Optional[User]:
        """登录认证"""
        user = await self.get_by_user_name(user_name=user_name)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def logout(self, user: UserModel) -> None:
        """登出"""
    
    def is_active(self, user: Union[User, UserModel]) -> bool:
        """是否可用"""
        return user.is_active

    def is_superuser(self, user: Union[User, UserModel]) -> bool:
        """是否系统管理员"""
        return user.is_superuser
