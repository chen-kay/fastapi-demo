from app.api import deps
from app.api.api_v1.deps.enterp import (ApiEnterpCreate, ApiEnterpFilter,
                                        ApiEnterpList, ApiEnterpStatus,
                                        ApiEnterpType, ApiEnterpUpdate)
from app.core.exceptions import ExistsError, NotFoundError
from app.schemas.models.enterp import EnterpCreate, EnterpUpdate
from app.schemas.models.user import UserModel
from app.services.enterp import EnterpService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/", summary="获取企业列表", response_model=ApiEnterpList)
async def get_list(
    model: ApiEnterpFilter = Depends(ApiEnterpFilter),
    enterp_service: EnterpService = Depends(),
):
    """获取企业列表"""
    data, total = await enterp_service.enterp.get_enterp_list(
        domain=model.domain,
        name=model.name,
        short_name=model.short_name,
        expire_at=model.expire_at,
        is_active=model.is_active,
        keyword=model.keyword,
        page=model.page,
        page_size=model.page_size,
    )
    return ApiEnterpList(total=total, data=data)


@router.post("/", summary="新增企业信息", response_model=ApiEnterpType)
async def create(
    obj_in: ApiEnterpCreate,
    enterp_service: EnterpService = Depends(),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    """新增企业信息"""
    ins = await enterp_service.enterp.get_by_domain(obj_in.domain)
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
    ins = await enterp_service.enterp.get_by_id(enterp_id)
    return ins


@router.put("/{enterp_id}", summary="修改企业信息", response_model=ApiEnterpType)
async def update(
    enterp_id: int,
    obj_in: ApiEnterpUpdate,
    enterp_service: EnterpService = Depends(),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    ins = await enterp_service.enterp.get_by_id(enterp_id)
    if not ins:
        raise NotFoundError()
    model = EnterpUpdate(
        **obj_in.dict(exclude_unset=True),
    )
    ins = await enterp_service.update(ins, model=model, current=current)
    return ins


@router.put("/status/{enterp_id}", summary="修改企业状态", response_model=ApiEnterpType)
async def update_status(
    enterp_id: int,
    obj_in: ApiEnterpStatus,
    enterp_service: EnterpService = Depends(),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    ins = await enterp_service.enterp.get_by_id(enterp_id)
    if not ins:
        raise NotFoundError()
    ins = await enterp_service.update_status(
        ins,
        is_active=obj_in.is_active,
        current=current,
    )
    return ins


@router.delete("/{enterp_id}", summary="删除企业信息", response_model=ApiEnterpType)
async def delete(
    enterp_id: int,
    enterp_service: EnterpService = Depends(),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    ins = await enterp_service.enterp.get_by_id(enterp_id)
    if not ins or not await enterp_service.enterp.is_active(ins):
        # 企业不存在 or 企业非正常状态
        raise NotFoundError()
    ins = await enterp_service.delete(ins, current=current)
    return ins
