from app import schemas
from app.core import security
from app.core.config import settings
from app.services import CompanyService, UserService
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/login")


async def get_current_user(
    service: UserService = Depends(),
    token: str = Depends(reusable_oauth2),
) -> schemas.UserModel:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[security.ALGORITHM],
        )
        token_data = schemas.TokenPayload(**payload)
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
    company_service: CompanyService = Depends(),
    current_user: schemas.UserModel = Depends(get_current_user),
) -> schemas.UserModel:
    if not current_user.is_superuser:
        # 非超级管理员 查验企业状态
        company = await company_service.find_by_id(current_user.company_id)
        if not company_service.is_active(company):
            # 企业不可用
            raise HTTPException(status_code=400, detail="Inactive user")
    if not user_service.is_active(current_user):
        # 用户不可用
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    service: UserService = Depends(),
    current_user: schemas.UserModel = Depends(get_current_user),
) -> schemas.UserModel:
    if not service.is_superuser(current_user):
        # 非超级管理员
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
