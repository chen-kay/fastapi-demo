from typing import Any

from app.api import deps
from app.schemas.current import CurrentType
from app.schemas.models.user import UserModel
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/current", response_model=CurrentType)
def read_user_current(
    current_user: UserModel = Depends(deps.get_current_active_user),
) -> Any:
    model = CurrentType(**current_user.dict())
    model.authoritys = []
    return model
