from app.api import deps
from app.api.api_v1.endpoints import login, sysCom, sysDictData, sysDictType
# from app.api.api_v1.endpoints import current, enterp, group, login
from fastapi import APIRouter, Depends

# , sysCom, sysDictData, sysDictType, sysOrg


api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(
    sysCom.router,
    tags=["sysCom"],
    prefix="/sysCom",
    dependencies=[Depends(deps.get_current_active_superuser)],
)
api_router.include_router(
    sysDictType.router,
    tags=["sysDictType"],
    prefix="/sysDictType",
    dependencies=[Depends(deps.get_current_active_user)],
)
api_router.include_router(
    sysDictData.router,
    tags=["sysDictData"],
    prefix="/sysDictData",
    dependencies=[Depends(deps.get_current_active_user)],
)
# api_router.include_router(
#     sysOrg.router,
#     tags=["sysOrg"],
#     prefix="/sysOrg",
#     dependencies=[Depends(deps.get_current_active_user)],
# )
