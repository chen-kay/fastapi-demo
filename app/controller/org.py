from app import schemas
from app.api import auth
from app.core import exceptions
from app.models import Org
from app.services import OrgService, UserService
from fastapi import Depends


class OrgController:
    def __init__(
        self,
        user_service: UserService = Depends(),
        org_service: OrgService = Depends(),
        current: schemas.UserModel = Depends(auth.get_current_active_user),
    ):
        self.user = user_service
        self.org = org_service
        self.current = current

    async def get_list(self, filters: schemas.OrgQuery):
        """获取机构列表"""
        qs = await self.org.get_list(
            name=filters.name,
            parent_id=filters.parent_id,
        )
        total = qs.count()
        qs = qs.offset((filters.page - 1) * filters.page_size).limit(filters.page_size)
        return qs.all(), total

    async def get_tree_list(self):
        """获取机构树"""
        return await self.org.get_tree_list()

    async def add(self, model: schemas.OrgAdd):
        """新增机构"""
        current = self.current
        company_id = None
        if not self.user.is_superuser(current):
            company_id = company_id
        else:
            company_id = company_id
        if await self.org.check_code_exists(
            model.code,
            company_id=company_id,
            parent_id=model.parent_id,
        ):
            raise exceptions.ExistsError()
        if await self.org.check_name_exists(
            model.name,
            company_id=company_id,
            parent_id=model.parent_id,
        ):
            raise exceptions.ExistsError()
        await self.org.add(model)
        return True

    async def edit(self, ins: Org, *, model: schemas.OrgEdit):
        """编辑机构"""
        if await self.org.check_code_exists(
            model.code,
            ins=ins,
            company_id=ins.company_id,
            parent_id=model.parent_id,
        ):
            raise exceptions.ExistsError()
        if await self.org.check_name_exists(
            model.name,
            ins=ins,
            company_id=ins.company_id,
            parent_id=model.parent_id,
        ):
            raise exceptions.ExistsError()

        await self.org.edit(ins, model=model)

    async def delete(self, ins: Org):
        """删除机构"""
        await self.org.delete(ins)

    async def export(self, filters: schemas.OrgQuery):
        """导出机构列表"""
        qs = await self.org.get_list(
            name=filters.name,
            parent_id=filters.parent_id,
        )
        return qs
