from app.api import deps
from app.api.api_v1.endpoints import current, enterp, login
from fastapi import APIRouter, Depends

api_router = APIRouter()
api_router.include_router(login.router, tags=["登录"])
api_router.include_router(
    current.router,
    tags=["用户信息"],
    dependencies=[Depends(deps.get_current_active_user)],
)
api_router.include_router(
    enterp.router,
    tags=["企业管理"],
    dependencies=[Depends(deps.get_current_active_superuser)],
)
