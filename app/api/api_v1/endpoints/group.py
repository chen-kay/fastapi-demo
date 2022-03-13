from app.api import deps
from app.api.api_v1.deps.group import (ApiGroupCreate, ApiGroupList,
                                       ApiGroupType, ApiGroupUpdate)
from app.core.exceptions import ExistsError, NotFoundError
from app.schemas.models.group import GroupCreate, GroupUpdate
from app.schemas.models.user import UserModel
from app.services.group import GroupService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/", summary="获取用户组列表", response_model=ApiGroupList)
async def get_list(
    group_service: GroupService = Depends(),
):
    """获取用户组列表"""
    data, _ = await group_service.get_group_list()
    data = await group_service.get_tree_data(data)
    return dict(data=data)


@router.post("/", summary="新增用户组信息", response_model=ApiGroupType)
async def create(
    obj_in: ApiGroupCreate,
    group_service: GroupService = Depends(),
    current: UserModel = Depends(deps.get_current_active_user),
):
    """新增用户组信息"""
    ins = await group_service.get_by_name(obj_in.name, pid_id=obj_in.pid_id)
    if ins:
        raise ExistsError(f"用户组: {obj_in.name} 已存在.")

    model = GroupCreate(
        **obj_in.dict(exclude_unset=True),
    )
    ins = await group_service.create(model=model, current=current)
    return ins


@router.get("/{group_id}", summary="获取用户组信息", response_model=ApiGroupType)
async def retrieve(
    group_id: int,
    group_service: GroupService = Depends(),
):
    """获取用户组信息"""
    ins = await group_service.get_by_id(group_id)
    return ins


@router.put("/{group_id}", summary="修改用户组信息", response_model=ApiGroupType)
async def update(
    group_id: int,
    obj_in: ApiGroupUpdate,
    group_service: GroupService = Depends(),
    current: UserModel = Depends(deps.get_current_active_user),
):
    ins = await group_service.get_by_id(group_id)
    model = GroupUpdate(
        **obj_in.dict(exclude_unset=True),
    )
    ins = await group_service.update(ins, model=model, current=current)
    return ins


@router.delete("/{group_id}", summary="删除用户组信息", response_model=ApiGroupType)
async def delete(
    group_id: int,
    group_service: GroupService = Depends(),
    current: UserModel = Depends(deps.get_current_active_user),
):
    ins = await group_service.get_by_id(group_id)
    if not ins:
        raise NotFoundError()
    ins = await group_service.delete(ins, current=current)
    return ins
