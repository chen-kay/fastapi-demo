from app.api import auth
from app.api.api_v1.endpoints import login, sysDict

# from app.api.api_v1.endpoints import current, enterp, group, login
from fastapi import APIRouter, Depends

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(
    sysDict.router,
    tags=["sysDict"],
    dependencies=[Depends(auth.get_current_active_user)],
)
# api_router.include_router(
#     group.router,
#     tags=["group"],
#     prefix="/group",
#     dependencies=[Depends(deps.get_current_active_user)],
# )
# api_router.include_router(
#     current.router,
#     tags=["current"],
#     dependencies=[Depends(deps.get_current_active_user)],
# )
# api_router.include_router(
#     enterp.router,
#     tags=["enterp"],
#     prefix="/enterp",
#     dependencies=[Depends(deps.get_current_active_superuser)],
# )
# api_router.include_router(
#     group.router,
#     tags=["group"],
#     prefix="/group",
#     dependencies=[Depends(deps.get_current_active_user)],
# )
