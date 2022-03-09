from app.api import deps
from app.api.api_v1.deps.enterp import (
    ApiEnterpCreate,
    ApiEnterpFilter,
    ApiEnterpList,
    ApiEnterpType,
    ApiEnterpUpdate,
)
from app.core.exceptions import ExistsError, NotFoundError
from app.schemas.models.enterp import EnterpCreate, EnterpFilter, EnterpUpdate
from app.schemas.models.user import UserModel
from app.services.enterp import EnterpService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/", summary="获取企业列表", response_model=ApiEnterpList)
async def get_list(
    filters: ApiEnterpFilter = Depends(ApiEnterpFilter),
    enterp_service: EnterpService = Depends(),
):
    """获取企业列表"""
    model = EnterpFilter(
        domain=filters.domain,
        name=filters.name,
        short_name=filters.short_name,
        expire_at=filters.expire_at,
        is_active=filters.is_active,
        page=filters.page,
        page_size=filters.page_size,
        keyword=filters.keyword,
    )
    data, total = await enterp_service.get_enterp_list(model)
    return ApiEnterpList(total=total, data=data)


@router.post("/", summary="新增企业信息", response_model=ApiEnterpType)
async def create(
    obj_in: ApiEnterpCreate,
    enterp_service: EnterpService = Depends(),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    """新增企业信息"""
    ins = await enterp_service.get_by_domain(obj_in.domain)
    if ins:
        raise ExistsError(f"域名: {obj_in.domain} 已存在.")

    model = EnterpCreate(
        **obj_in.dict(exclude_unset=True),
    )
    ins = await enterp_service.create(model=model, current=current)
    return ins


@router.get("/{enterp_id}", summary="获取企业信息", response_model=ApiEnterpType)
async def retrieve(
    enterp_id: int,
    enterp_service: EnterpService = Depends(),
):
    """获取企业信息"""
    ins = await enterp_service.get_by_id(enterp_id)
    return ins


@router.put("/{enterp_id}", summary="修改企业信息", response_model=ApiEnterpType)
async def update(
    enterp_id: int,
    obj_in: ApiEnterpUpdate,
    enterp_service: EnterpService = Depends(),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    ins = await enterp_service.get_by_id(enterp_id)
    if not ins:
        raise NotFoundError()
    model = EnterpUpdate(
        **obj_in.dict(exclude_unset=True),
    )
    ins = await enterp_service.update(ins, model=model, current=current)
    return ins


@router.delete("/{enterp_id}", summary="删除企业信息", response_model=ApiEnterpType)
async def delete(
    enterp_id: int,
    enterp_service: EnterpService = Depends(),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    ins = await enterp_service.get_by_id(enterp_id)
    if not ins:
        raise NotFoundError()
    ins = await enterp_service.delete(ins, current=current)
    return ins
