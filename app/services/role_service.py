from typing import Optional

from app import schemas
from app.models import Role, User, UserRole
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import or_

from .base import BaseService


class RoleService(BaseService["Role"]):
    async def get_list(
        self,
        db: Session,
        *,
        company_id: int = None,
        name: str = None,
        keyword: str = None,
    ):
        qs = self.get_queryset(db).filter(
            Role.is_del == 0, Role.company_id == company_id
        )
        if name:
            qs = qs.filter(Role.name.like(name))
        if keyword:
            qs = qs.filter(
                or_(
                    Role.name.like(f"%{keyword}%"),
                    Role.code.like(f"%{keyword}%"),
                )
            )
        return qs

    def get_pagination(self, data: Query, *, page: int, limit: int):
        return self.pagination(data, page=page, limit=limit)

    async def get_by_id(self, db: Session, *, id: int) -> Optional[Role]:
        """从数据库获取组织 - 组织id"""
        qs = db.query(Role).filter(
            Role.is_del == 0,
            Role.id == id,
        )
        ins = qs.first()
        return ins

    async def add(self, db: Session, *, model: schemas.RoleAdd):
        """新增组织"""
        ins = await self.create(db, model=model.dict())
        return ins

    async def edit(
        self,
        db: Session,
        *,
        ins: Role,
        model: schemas.RoleEdit,
    ):
        """修改组织"""
        ins = await self.update(db, ins=ins, model=model.dict(exclude_unset=True))
        return ins

    async def delete(self, db: Session, *, ins: Role):
        """删除角色"""
        ins = await self.update(db, ins=ins, model=dict(is_del=1))
        return ins

    async def grant_menu(self, db: Session, *, ins: Role, model: schemas.RoleGrantMenu):
        """设置角色权限"""
        ins.access = model.access_ids
        db.add(ins)
        db.flush()

    async def grant_data(self, db: Session, *, ins: Role, model: schemas.RoleGrantData):
        """设置角色数据"""
        ins = await self.update(
            db, ins=ins, model=dict(dataScopeType=model.dataScopeType)
        )
        return ins

    async def check_code_exists(
        self,
        db: Session,
        *,
        code: str,
        ins: Role = None,
    ):
        """验证编码是否存在"""
        qs = db.query(Role).filter(Role.code == code, Role.is_del == 0)
        if ins:
            qs = qs.filter(Role.id != ins.id)
        return db.query(qs.exists()).scalar()

    async def check_name_exists(
        self,
        db: Session,
        *,
        name: str,
        ins: Role = None,
    ):
        """验证名称是否存在"""
        qs = db.query(Role).filter(Role.name == name, Role.is_del == 0)
        if ins:
            qs = qs.filter(Role.id != ins.id)
        return db.query(qs.exists()).scalar()

    async def check_user_exists(self, db: Session, *, role_id: int):
        """验证是否存在用户"""
        qs = (
            db.query(UserRole)
            .join(User)
            .filter(UserRole.role_id == role_id, User.is_del == 0)
        )
        return qs.exists()


role = RoleService(Role)
