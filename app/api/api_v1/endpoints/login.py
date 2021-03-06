from app import schemas, services
from app.core import security
from app.core.exceptions import APIException
from app.db.deps import get_session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", summary="登录认证", response_model=schemas.Token)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = await services.user.authenticate(
        db, user_name=data.username, password=data.password
    )
    if not user or not services.user.is_active(user):
        raise APIException("用户名密码错误")

    access_token = security.create_access_token(user.id)
    # todo
    # 登录成功 记录登录日志
    # 是否限制单用户登录
    return dict(
        access_token=access_token,
        token_type="Bearer",
    )


@router.post("/logout", summary="退出登录", response_model=schemas.Msg)
async def logout():
    # todo
    # 清除登录会话
    # 创建退出登录日志
    return dict(msg="操作成功")
