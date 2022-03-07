from typing import Optional

from app import models
from app.core import security
from app.core.config import settings
from app.schemas.models.user import UserModel
from app.services.enterp import EnterpService
from app.services.user import UserService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel, ValidationError

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/login")


class TokenPayload(BaseModel):
    sub: Optional[int] = None


async def get_current_user(
    service: UserService = Depends(),
    token: str = Depends(reusable_oauth2),
) -> UserModel:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await service.find_by_id(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    user_service: UserService = Depends(),
    enterp_service: EnterpService = Depends(),
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not current_user.is_superuser:
        # 非超级管理员 查验企业状态
        enterp = await enterp_service.find_by_id(current_user.enterp_id)
        if not await enterp_service.is_active(enterp):
            # 企业不可用
            raise HTTPException(status_code=400, detail="Inactive user")
    if not await user_service.is_active(current_user):
        # 用户不可用
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    service: UserService = Depends(),
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not await service.is_superuser(current_user):
        # 非超级管理员
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
