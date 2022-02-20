from app.api import deps
from app.api.api_v1.deps.enterp import ApiEnterpCreate, ApiEnterpType
from app.api.db import get_services
from app.core.exceptions import APIException
from app.schemas.models.enterp import EnterpCreate
from app.schemas.models.user import UserModel
from app.services.enterp import EnterpService
from fastapi import APIRouter, Depends

router = APIRouter()


# @router.get("/", summary="获取企业列表", response_model=EnterpList)
# async def get_list(
#     filters: EnterpFilter = Depends(get_enterp_filters),
#     enterp_service: EnterpService = Depends(
#         get_services(EnterpService),
#     ),
# ):
#     enterps, total = await enterp_service.get_enterp_list(
#         keyword=filters.keyword,
#         page=filters.page,
#         page_size=filters.page_size,
#     )
#     return EnterpList(total=total, data=enterps)


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
        **obj_in.dict(),
        add_user_id=current.id,
        alt_user_id=current.id,
    )
    enterp = await enterp_service.create(model)
    return enterp


@router.get("/{enterp_id}", summary="获取企业信息", response_model=ApiEnterpType)
async def create(
    enterp_id: int,
    enterp_service: EnterpService = Depends(get_services(EnterpService)),
):
    """新增企业信息"""
    enterp = await enterp_service.get_by_id(enterp_id)
    return enterp
