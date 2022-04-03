from aioredis import Redis
from app import schemas, services
from app.core import security
from app.core.config import settings
from app.db.deps import get_redis, get_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"/login")


async def get_current_user(
    db: Session = Depends(get_session),
    redis: Redis = Depends(get_redis),
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
    user = await services.user.find_by_id(
        db,
        id=token_data.sub,
        redis=redis,
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    db: Session = Depends(get_session),
    redis: Redis = Depends(get_redis),
    current_user: schemas.UserModel = Depends(get_current_user),
) -> schemas.UserModel:
    if not current_user.is_superuser:
        # 非超级管理员 查验企业状态
        company = await services.company.find_by_id(
            db,
            current_user.company_id,
            redis=redis,
        )
        if not services.company.is_active(company):
            # 企业不可用
            raise HTTPException(status_code=400, detail="Inactive user")
    if not services.user.is_active(current_user):
        # 用户不可用
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: schemas.UserModel = Depends(get_current_user),
) -> schemas.UserModel:
    if not services.user.is_superuser(current_user):
        # 非超级管理员
        raise HTTPException(
            status_code=401, detail="The user doesn't have enough privileges"
        )
    return current_user
