from app.api import deps
from app.api.db import get_services
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


@router.post("/", summary="新增企业信息", response_model=EnterpType)
async def create(
    obj_in: CreateForm,
    enterp_service: EnterpService = Depends(get_services(EnterpService)),
    current: UserModel = Depends(deps.get_current_active_superuser),
):
    """新增企业信息"""
    enterp = await enterp_service.create(obj_in, current)
    return enterp
