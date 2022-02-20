from datetime import timedelta

from app.api.deps import get_services
from app.core import security
from app.core.config import settings
from app.core.exceptions import APIException
from app.schemas.login import LoginType
from app.services.user import UserService
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login/account", summary="登录认证", response_model=LoginType)
async def login_access_token(
    data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_services(UserService)),
):
    user_name = data.username
    user = await user_service.authenticate(user_name=user_name, password=data.password)
    if not user or not await user_service.is_active(user):
        raise APIException("用户名密码错误")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return dict(
        status="ok",
        access_token=access_token,
        token_type="Bearer",
    )
