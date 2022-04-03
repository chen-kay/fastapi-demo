import json
from datetime import date
from typing import List, Optional, Union

from aioredis import Redis
from app import schemas
from app.models import Company
from sqlalchemy.orm import Query, Session
from sqlalchemy.sql import or_

from .base import BaseService


class CompanyService(BaseService["Company"]):
    async def get_filter(
        self,
        db: Session,
        *,
        status: Optional[int] = None,
        expire_at: Optional[List[date]] = None,
        keyword: Optional[str] = None,
    ) -> Query:
        """获取企业列表"""
        qs = (
            self.get_queryset(db)
            .filter(Company.is_del == 0)
            .order_by(Company.id.desc())
        )
        if status:
            qs = qs.filter(Company.status == status)
        if expire_at:
            qs = qs.filter(Company.expire_at.between(expire_at[0], expire_at[1]))
        if keyword:
            qs = qs.filter(
                or_(
                    Company.domain.like(f"%{keyword}%"),
                    Company.name.like(f"%{keyword}%"),
                    Company.short_name.like(f"%{keyword}%"),
                )
            )
        return qs

    def get_pagination(self, data: Query, *, page: int, limit: int):
        return self.pagination(data, page=page, limit=limit)

    async def add(
        self,
        db: Session,
        *,
        model: schemas.CompanyAdd,
    ):
        """新增企业"""
        ins = await self.create(db, model=model.dict())
        if self.is_expire(ins):
            ins.status = 3
            db.flush()
        return ins

    async def edit(
        self,
        db: Session,
        *,
        ins: Company,
        model: schemas.CompanyEdit,
        redis: Redis = None,
    ):
        """修改企业"""
        ins = await self.update(db, ins=ins, model=model.dict(exclude_unset=True))
        if self.is_expire(ins):
            ins.status = 3
            db.flush()
        await self.clear_cache(ins, redis=redis)
        return ins

    async def delete(self, db: Session, *, ins: Company, redis: Redis = None):
        """删除企业"""
        ins = await self.update(db, ins=ins, model=dict(is_del=1))
        await self.clear_cache(ins, redis=redis)
        return ins

    async def clear_cache(self, ins: Company, *, redis: Redis = None):
        if not redis:
            return
        await redis.delete(f"enterp:id:{id}")

    async def get_by_id(self, db: Session, *, id: int) -> Optional[Company]:
        """从数据库获取企业 - 企业id"""
        qs = db.query(Company).filter(
            Company.is_del == 0,
            Company.id == id,
        )
        ins = qs.first()
        return ins

    async def find_by_id(
        self,
        db: Session,
        *,
        id: int,
        redis: Redis = None,
    ) -> schemas.CompanyModel:
        """从缓存获取企业 - 企业id"""
        key = f"enterp:id:{id}"
        if redis and await redis.exists(key):
            user_str = await redis.get(key)
            user_dict = json.loads(user_str)
            model = schemas.CompanyModel(**user_dict)
        else:
            ins = await self.get_by_id(db, id=id)
            model = schemas.CompanyModel.from_orm(ins)
            redis and await redis.set(key, json.dumps(model.dict(), ensure_ascii=False))
        return model

    async def check_domain_exists(
        self,
        db: Session,
        *,
        domain: str,
        ins: Company = None,
    ):
        """验证编码是否存在"""
        qs = db.query(Company).filter(Company.domain == domain, Company.is_del == 0)
        if ins:
            qs = qs.filter(Company.id != ins.id)
        return db.query(qs.exists()).scalar()

    async def check_name_exists(
        self,
        db: Session,
        *,
        name: str,
        ins: Company = None,
    ):
        """验证名称是否存在"""
        qs = db.query(Company).filter(Company.name == name, Company.is_del == 0)
        if ins:
            qs = qs.filter(Company.id != ins.id)
        return db.query(qs.exists()).scalar()

    def is_active(self, ins: Union[Company, schemas.CompanyModel]) -> bool:
        """企业是否可用"""
        return ins.is_del == 0 and ins.status == 1

    def is_expire(self, ins: Union[Company, schemas.CompanyModel]):
        """企业是否过期"""
        now = date.today()
        return ins.expire_at and ins.expire_at < now


company = CompanyService(Company)
