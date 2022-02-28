from app.models import Group
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from .base import BaseCrud


class GroupCrud(BaseCrud[Group]):
    async def get_group_list(self, session: Session):
        qs = session.query(Group).filter(Group.is_del == 0)
        total = qs.count()
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
