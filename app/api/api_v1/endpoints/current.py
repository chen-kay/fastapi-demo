from typing import Any

from app.api import deps
from app.core.exceptions import NotFoundError
from app.schemas.current import CurrentType
from app.schemas.models.user import UserModel
from app.services.user import UserService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/current", summary="获取当前用户信息", response_model=CurrentType)
async def read_user_current(
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    model = CurrentType(**current_user.dict())
    model.access = []
    return model


@router.post("/passwd", summary="修改当前用户密码", response_model=CurrentType)
async def change_current_passwd(
    password: str,
    current_user: UserModel = Depends(deps.get_current_active_user),
    user_service: UserService = Depends(),
) -> Any:
    ins = await user_service.get_by_id(current_user.id)
    if not ins:
        raise NotFoundError()
    ins = await user_service.set_password(ins, password)
    return ins
