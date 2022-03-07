from app.models import Group

from .base import BaseCrud


class GroupCrud(BaseCrud[Group]):
    async def get_group_list(self):
        qs = self.session.query(Group).filter(Group.is_del == 0)
        total = qs.count()
        return qs, total

    async def get_by_name(
        self,
        name: str,
        *,
        pid_id: int = None,
    ):
        qs = self.session.query(Group).filter(
            Group.is_del == 0,
            Group.name == name,
            Group.pid_id == pid_id,
        )
        ins = qs.first()
        return ins
