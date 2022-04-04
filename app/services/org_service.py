import json
from typing import Dict, List, Optional

from aioredis import Redis
from app import schemas
from app.models import Org, User
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import or_

from .base import BaseService


class OrgService(BaseService["Org"]):
    async def get_list(
        self,
        db: Session,
        *,
        company_id: int = None,
        parent_id: int = None,
        parent_ids: List[int] = None,
        name: str = None,
        keyword: str = None,
        ids: List[int] = None,
    ):
        qs = self.get_queryset(db).filter(Org.is_del == 0, Org.company_id == company_id)
        if ids:
            qs = qs.filter(Org.id.in_(ids))
        if parent_id:
            if parent_ids:
                qs = qs.filter(or_(Org.parent_id.in_(parent_ids), Org.id == parent_id))
            else:
                qs = qs.filter(Org.parent_id == parent_id)
        if name:
            qs = qs.filter(Org.name.like(name))
        if keyword:
            qs = qs.filter(
                or_(
                    Org.name.like(f"%{keyword}%"),
                    Org.code.like(f"%{keyword}%"),
                )
            )
        return qs

    def get_pagination(self, data: Query, *, page: int, limit: int):
        return self.pagination(data, page=page, limit=limit)

    def get_list_data(self, data: List[Org], org_data: Dict[str, schemas.OrgModel]):
        for item in data:
            item.parent_ids = self.get_parent_ids(item.id, org_data)
        return data

    def get_tree_data(self, data: Dict[str, schemas.OrgModel], parent_id: int = 0):
        """获取组织树"""
        result: List[schemas.OrgTree] = []
        for item in data.values():
            model = schemas.OrgTree(**item.dict())
            if model.parent_id != parent_id:
                continue
            chil = self.get_tree_data(data, parent_id=model.id)
            if chil:
                model.children = chil
            result.append(model)
        return result

    async def get_by_id(self, db: Session, *, id: int) -> Optional[Org]:
        """从数据库获取组织 - 组织id"""
        qs = db.query(Org).filter(
            Org.is_del == 0,
            Org.id == id,
        )
        ins = qs.first()
        return ins

    async def add(self, db: Session, *, model: schemas.OrgAdd):
        """新增组织"""
        ins = await self.create(db, model=model.dict())
        return ins

    async def edit(
        self,
        db: Session,
        *,
        ins: Org,
        model: schemas.OrgEdit,
    ):
        """修改组织"""
        ins = await self.update(db, ins=ins, model=model.dict(exclude_unset=True))
        return ins

    async def delete(self, db: Session, *, ins: Org):
        """删除组织"""
        ins = await self.update(db, ins=ins, model=dict(is_del=1))
        return ins

    async def check_code_exists(
        self,
        db: Session,
        *,
        code: str,
        ins: Org = None,
    ):
        """验证编码是否存在"""
        qs = db.query(Org).filter(Org.code == code, Org.is_del == 0)
        if ins:
            qs = qs.filter(Org.id != ins.id)
        return qs.exists()

    async def check_name_exists(
        self,
        db: Session,
        *,
        name: str,
        ins: Org = None,
    ):
        """验证名称是否存在"""
        qs = db.query(Org).filter(Org.name == name, Org.is_del == 0)
        if ins:
            qs = qs.filter(Org.id != ins.id)
        return qs.exists()

    async def check_user_exists(self, db: Session, *, org_ids: List[int]):
        """验证是否存在用户"""
        qs = db.query(User).filter(User.org_id.in_(org_ids), User.is_del == 0)
        return qs.exists()

    async def get_org_data(
        self,
        db: Session,
        *,
        company_id: int,
        redis: Redis = None,
    ) -> Dict[str, schemas.OrgModel]:
        key = f"org:data:{company_id}"
        if redis and await redis.exists(key):
            data = json.loads(await redis.get(key))
            model = {key: schemas.OrgModel(**val) for key, val in data.items()}
        else:
            qs = await self.get_list(db, company_id=company_id)
            model = {r.id: schemas.OrgModel.from_orm(r) for r in qs}
            redis and await redis.set(key, json.dumps(model, ensure_ascii=False))
        return model

    def get_parent_ids(self, org_id: int, data: Dict[str, schemas.OrgModel]):
        org = data.get(org_id, None)
        if not org or not org.parent_id:
            return []
        return self.get_parent_ids(org.parent_id, data) + [org.parent_id]

    def get_sub_org_ids(self, org_id: int, data: Dict[str, schemas.OrgModel]):
        arrIds = set([org_id]) if org_id else set([])
        for item in data.values():
            if item.parent_id == org_id:
                subIds = self.get_sub_org_ids(item.id, data)
                if subIds:
                    arrIds |= subIds
        return arrIds


org = OrgService(Org)
