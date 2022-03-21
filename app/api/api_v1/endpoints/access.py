from typing import Any

from app.api import deps
from app.schemas.current import CurrentType
from app.schemas.models.user import UserModel
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/access", summary="获取系统权限", response_model=CurrentType)
async def read_user_current(
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    model = CurrentType(**current_user.dict())
    model.access = []
    return model
