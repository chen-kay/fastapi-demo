import json
from typing import Optional, Union

from aioredis import Redis
from app import schemas
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import Company, User
from sqlalchemy.orm import Session

from .base import BaseService


class UserService(BaseService["User"]):
    async def add(
        self,
        db: Session,
        *,
        model: schemas.UserAdd,
        is_superuser: int = 0,
        is_admin: int = 0,
        user_name: str = None,
    ):
        create_data = model.dict(exclude={"password"})
        create_data["hashed_password"] = get_password_hash(model.password)
        create_data["is_superuser"] = is_superuser
        create_data["is_admin"] = is_admin
        if user_name:
            create_data["user_name"] = user_name
        return await self.create(db, model=create_data)

    async def create_admin_user(self, db: Session, *, ins: Company):
        user_name = f"{settings.FIRST_ADMINUSER}@{ins.domain}"
        model = schemas.UserAdd(
            company_id=ins.id,
            username=settings.FIRST_ADMINUSER,
            fullname="系统管理员",
            nickname="管理员",
            password=settings.FIRST_ADMIN_PASSWORD,
            is_admin=1,
        )
        ins = await self.add(
            db,
            model=model,
            is_admin=1,
            user_name=user_name,
        )
        return ins

    async def get_by_id(self, db: Session, *, id: int) -> Optional[User]:
        """从数据库获取用户 - 用户id"""
        qs = db.query(User).filter(
            User.is_del == 0,
            User.id == id,
        )
        ins = qs.first()
        return ins

    async def find_by_id(
        self, db: Session, id: int, redis: Optional[Redis] = None
    ) -> schemas.UserModel:
        """从缓存获取用户 - 用户id"""
        key = f"user:id:{id}"
        if redis and await redis.exists(key):
            user_str = await redis.get(key)
            user_dict = json.loads(user_str)
            model = schemas.UserModel(**user_dict)
        else:
            ins = await self.get_by_id(db, id=id)
            model = schemas.UserModel.from_orm(ins)
            redis and await redis.set(key, json.dumps(model.dict(), ensure_ascii=False))
        return model

    async def get_by_user_name(self, db: Session, *, user_name: str) -> Optional[User]:
        """从数据库获取用户 - 用户账号"""
        qs = db.query(User).filter(
            User.is_del == 0,
            User.user_name == user_name,
        )
        ins = qs.first()
        return ins

    async def authenticate(self, db: Session, *, user_name: str, password: str) -> User:
        """用户认证"""
        user = await self.get_by_user_name(db, user_name=user_name)
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

    def is_admin(self, user: Union[User, schemas.UserModel]) -> bool:
        """是否管理员"""
        return bool(user.is_admin)

    def is_superuser(self, user: Union[User, schemas.UserModel]) -> bool:
        """用户是否超级管理员"""
        return bool(user.is_superuser)

    async def check_user_company(
        self, user: Union[User, schemas.UserModel], company_id: int
    ):
        if self.is_superuser(user):
            return True
        return user.company_id == company_id


user = UserService(User)
