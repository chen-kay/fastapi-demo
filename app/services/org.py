import json
from typing import List, Optional, Tuple

from app import schemas
from app.models import Org

from .base import BaseService


class OrgService(BaseService["Org"]):
    model = Org

    async def get_list(
        self,
        *,
        name: str = None,
        parent_id: int = None,
        status: int = None,
    ):
        """获取组织列表"""
        qs = self.session.query(Org).filter(Org.is_del == 0).order_by(Org.sort)
        if name:
            qs = qs.filter(Org.name == name)
        if parent_id:
            qs = qs.filter(Org.parent_id == parent_id)
        if status:
            qs = qs.filter(Org.status == status)
        return qs

    async def get_tree_list(self) -> List[Org]:
        """获取组织树"""
        qs = await self.get_list(status=1)
        return self.render_children(list(qs))

    def render_children(self, data: List[Org], parent_id: int = 0):
        res = []
        for item in data:
            print(item.parent)
            if item.parent_id != parent_id:
                continue
            children = self.render_children(data, parent_id=item.id)
            item.children = children
            res.append(item)
        return res

    async def add(self, model: schemas.OrgAdd):
        """新增组织"""
        data = model.dict(exclude_unset=True)
        ins = await self.create(data)
        return ins

    async def edit(self, ins: Org, *, model: schemas.OrgEdit):
        """修改组织"""
        data = model.dict(exclude_unset=True)
        ins = await self.update(ins, model=data)
        return ins

    async def get_by_id(self, id: int) -> Optional[Org]:
        """从数据库获取组织 - 组织id"""
        qs = self.session.query(Org).filter(
            Org.is_del == 0,
            Org.id == id,
        )
        ins = qs.first()
        return ins

    async def check_code_exists(
        self,
        code: str,
        *,
        company_id: int,
        ins: Org = None,
        parent_id: int = None,
    ):
        """验证编码是否存在"""
        qs = self.session.query(Org).filter(
            Org.code == code,
            Org.is_del == 0,
            Org.company_id == company_id,
        )
        if ins:
            qs = qs.filter(Org.id != ins.id)
        if parent_id:
            qs = qs.filter(Org.parent_id == parent_id)
        return self.session.query(qs.exists()).scalar()

    async def check_name_exists(
        self,
        name: str,
        *,
        company_id: int,
        ins: Org = None,
        parent_id: int = None,
    ):
        """验证名称是否存在"""
        qs = self.session.query(Org).filter(
            Org.name == name,
            Org.is_del == 0,
            Org.company_id == company_id,
        )
        if ins:
            qs = qs.filter(Org.id != ins.id)
        if parent_id:
            qs = qs.filter(Org.parent_id == parent_id)

        return self.session.query(qs.exists()).scalar()
