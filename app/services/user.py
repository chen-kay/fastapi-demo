"""User Services module."""

import json
from typing import Optional, Union

from app.core.security import get_password_hash, verify_password
from app.models import User
from app.schemas.models.user import UserCreate, UserModel

from .base import BaseService


class UserService(BaseService):
    async def get_by_user_name(self, user_name: str):
        user = (
            self.session.query(User)
            .filter(User.user_name == user_name, User.is_del == 0)
            .first()
        )
        return user

    async def get_by_id(self, id: int):
        user = self.session.query(User).filter(User.id == id, User.is_del == 0).first()
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
            ins = await self.get_by_id(id=id)
            user = UserModel.from_orm(ins)
            self.redis and await self.redis.set(
                key, json.dumps(user.dict(), ensure_ascii=False)
            )
        return user

    async def authenticate(self, user_name: str, password: str) -> Optional[User]:
        """登录认证"""
        user = await self.get_by_user_name(user_name=user_name)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def logout(self, user: UserModel) -> None:
        """登出"""

    async def is_active(self, user: Union[User, UserModel]) -> bool:
        """是否可用"""
        return user.is_active

    async def is_superuser(self, user: Union[User, UserModel]) -> bool:
        """是否系统管理员"""
        return user.is_superuser

    async def create(self, model: UserCreate, is_superuser: int = 0):
        """创建用户"""
        create_data = model.dict(exclude_unset=True, exclude={"password"})
        ins = User(**create_data)
        ins.is_superuser = is_superuser
        ins.hashed_password = get_password_hash(model.password)

        self.session.add(ins)
        self.session.commit()
        self.session.refresh(ins)

    async def create_superuser(self, model: UserCreate):
        """创建超级管理员"""
        return self.create(model, is_superuser=1)
