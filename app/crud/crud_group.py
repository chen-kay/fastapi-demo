from app.models import Group

from .base import BaseCrud


class GroupCrud(BaseCrud[Group]):
    model = Group

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

    async def get_name_exist(
        self, name: str, *, pid_id: int = None, group_id: int = None
    ):
        qs = self.session.query(Group).filter(
            Group.is_del == 0,
            Group.name == name,
            Group.pid_id == pid_id,
        )
        if group_id:
            qs = qs.filter(Group.id != group_id)
        ins = qs.first()
        return ins
