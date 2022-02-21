from app.api import deps
from app.api.api_v1.deps.enterp import (
    ApiEnterpCreate,
    ApiEnterpFilter,
    ApiEnterpList,
    ApiEnterpType,
    ApiEnterpUpdate,
)
from app.api.db import get_services
from app.core.exceptions import APIException
from app.schemas.models.enterp import EnterpCreate, EnterpFilter, EnterpUpdate
from app.schemas.models.user import UserModel
from app.services.enterp import EnterpService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/", summary="获取企业列表", response_model=ApiEnterpList)
async def get_list(
    filters: ApiEnterpFilter = Depends(),
    enterp_service: EnterpService = Depends(get_services(EnterpService)),
):
    model = EnterpFilter(**filters.dict(exclude_unset=True))
    enterps, total = await enterp_service.get_enterp_list(model)
    return ApiEnterpList(total=total, data=enterps)


@router.post("/", summary="新增企业信息", response_model=ApiEnterpType)
async def create(
    obj_in: ApiEnterpCreate,
    enterp_service: EnterpService = Depends(get_services(EnterpService)),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    """新增企业信息"""
    enterp = await enterp_service.get_by_domain(obj_in.domain)
    if enterp:
        raise APIException(f"域名: {obj_in.domain} 已存在.")

    model = EnterpCreate(
        **obj_in.dict(exclude_unset=True),
        add_user_id=current.id,
        alt_user_id=current.id,
    )
    enterp = await enterp_service.create(model)
    return enterp


@router.get("/{enterp_id}", summary="获取企业信息", response_model=ApiEnterpType)
async def retrieve(
    enterp_id: int,
    enterp_service: EnterpService = Depends(get_services(EnterpService)),
):
    """获取企业信息"""
    enterp = await enterp_service.get_by_id(enterp_id)
    return enterp


@router.put("/{enterp_id}", summary="修改企业信息", response_model=ApiEnterpType)
async def update(
    enterp_id: int,
    obj_in: ApiEnterpUpdate,
    enterp_service: EnterpService = Depends(get_services(EnterpService)),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    enterp = await enterp_service.get_by_id(enterp_id)
    model = EnterpUpdate(
        **obj_in.dict(exclude_unset=True),
        alt_user_id=current.id,
    )
    enterp = await enterp_service.update(enterp, model)
    return enterp


@router.delete("/{enterp_id}", summary="删除企业信息", response_model=ApiEnterpType)
async def delete(
    enterp_id: int,
    enterp_service: EnterpService = Depends(get_services(EnterpService)),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    enterp = await enterp_service.get_by_id(enterp_id)
    model = EnterpUpdate(
        del_user_id=current.id,
    )
    enterp = await enterp_service.delete(enterp, model)
    return enterp
