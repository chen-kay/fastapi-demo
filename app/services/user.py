"""User Services module."""

from typing import Optional, Union

from app import crud
from app.core.security import get_password_hash, verify_password
from app.models import User
from app.schemas.models.user import UserCreate, UserModel

from .base import BaseService


class UserService(BaseService):
    def initializer(self):
        self.user = crud.User(self.session, self.redis)

    async def authenticate(self, user_name: str, password: str) -> Optional[User]:
        """登录认证"""
        user = await self.get_by_user_name(user_name)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def create(
        self,
        model: UserCreate,
        is_superuser: int = 0,
        current: Optional[UserModel] = None,
    ):
        """创建用户"""
        create_data = model.dict(exclude_unset=True, exclude={"password"})

        create_data["hashed_password"] = get_password_hash(model.password)
        create_data["is_superuser"] = is_superuser
        create_data["add_user_id"] = current.id or None
        create_data["alt_user_id"] = current.id or None

        return await self.user.create(create_data)

    async def create_superuser(self, model: UserCreate):
        """创建超级管理员"""
        return await self.create(model, is_superuser=1)

    async def set_password(self, ins: User, password: str):
        """修改密码"""
        data = dict(hashed_password=get_password_hash(password))
        ins = await self.user.update(ins, model=data)
        return ins

    async def logout(self, user: UserModel) -> None:
        """登出"""

    async def is_active(self, user: Union[User, UserModel]) -> bool:
        """是否可用"""
        return user.is_active

    async def is_superuser(self, user: Union[User, UserModel]) -> bool:
        """是否系统管理员"""
        return user.is_superuser

    async def get_by_user_name(self, user_name: str):
        return await self.user.get_by_user_name(user_name)

    async def get_by_id(self, id: int):
        return await self.user.get_by_id(id)

    async def find_by_user_name(self, user_name: str):
        return await self.user.find_by_user_name(user_name)

    async def find_by_id(self, id: int):
        return await self.user.find_by_id(id)
