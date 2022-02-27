from app.models import Group
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from .base import BaseCrud


class GroupCrud(BaseCrud[Group]):
    async def get_group_list(
        self,
        session: Session,
        *,
        keyword: str,
        page: int,
        page_size: int,
    ):
        qs = session.query(Group).filter(Group.is_del == 0)
        if keyword:
            qs = qs.filter(
                or_(
                    Group.name.like(f"%{keyword}%"),
                    Group.desc.like(f"%{keyword}%"),
                )
            )

        total = qs.count()
        qs = qs.offset((page - 1) * page_size).limit(page_size).all()
        return qs, total

    async def get_by_name(
        self,
        session: Session,
        *,
        name: str,
        pid_id: int = None,
    ):
        qs = session.query(Group).filter(
            Group.is_del == 0,
            Group.name == name,
            Group.pid_id == pid_id,
        )
        ins = qs.first()
        return ins


group = GroupCrud(Group)
