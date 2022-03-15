"""Group Services module."""

from typing import List, Optional

from app import crud
from app.models import Group
from app.schemas.models.group import GroupCreate, GroupUpdate
from app.schemas.models.user import UserModel

from .base import BaseService


class GroupService(BaseService):
    def initializer(self):
        self.group = crud.Group(self.session, self.redis)

    async def get_data(self):
        data, _ = await self.group.get_group_list()
        return await self.get_tree_data(data)

    async def get_cascader(self):
        data, _ = await self.group.get_group_list()
        return await self.get_tree_data(data)

    async def get_group_list(self):
        return await self.group.get_group_list()

    async def create(self, *, model: GroupCreate, current: UserModel):
        """创建用户组"""
        create_data = model.dict(exclude_unset=True)
        create_data["add_user_id"] = current.id
        create_data["alt_user_id"] = current.id

        ins = await self.group.create(create_data)
        return ins

    async def update(
        self,
        ins: Group,
        *,
        model: GroupUpdate,
        current: UserModel,
    ):
        """修改用户组"""
        update_data = model.dict(exclude_unset=True)
        update_data["alt_user_id"] = current.id

        ins = await self.group.update(ins, model=update_data)
        return ins

    async def delete(self, ins: Group, *, current: UserModel):
        """删除用户组"""
        update_data = dict(del_user_id=current.id)
        ins = await self.group.delete(ins, model=update_data)
        return ins

    async def get_tree_data(
        self, data: List[Group], pid_id: int = None, path: List[int] = []
    ):
        res: List[Group] = []
        for item in data:
            if item.pid_id != pid_id:
                continue
            item.path = path
            chil = await self.get_tree_data(data, pid_id=item.id, path=path + [item.id])
            if chil:
                item.children = chil
            res.append(item)
        return res
