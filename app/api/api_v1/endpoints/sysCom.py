from typing import List

from aioredis import Redis
from app import schemas, services
from app.core import exceptions
from app.db.deps import get_redis, get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/",
    summary="获取企业列表",
    response_model=schemas.Pageination[schemas.CompanyType],
)
async def list(
    filters: schemas.CompanyFilter = Depends(),
    db: Session = Depends(get_session),
):
    data = await services.company.get_filter(
        db,
        status=filters.status,
        expire_at=filters.expire_at,
        keyword=filters.keyword,
    )
    result, total = services.company.get_pagination(
        data,
        page=filters.page,
        limit=filters.page_size,
    )
    return dict(data=result, total=total)


@router.post(
    "/add",
    summary="新增企业",
    response_model=schemas.Msg,
)
async def add(
    model: schemas.CompanyAdd,
    db: Session = Depends(get_session),
):
    if await services.company.check_domain_exists(db, domain=model.domain):
        raise exceptions.ExistsError(f"域名[{model.domain}]已存在.")
    if await services.company.check_name_exists(db, name=model.name):
        raise exceptions.ExistsError(f"企业名称[{model.name}]已存在")

    try:
        # 创建企业
        ins = await services.company.add(db, model=model)
        # 创建企业管理员账户
        await services.user.create_admin_user(db, ins=ins)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return dict(msg="操作成功")


@router.put(
    "/edit/<int:pk>",
    summary="修改企业",
    response_model=schemas.Msg,
)
async def edit(
    pk: int,
    model: schemas.CompanyEdit,
    db: Session = Depends(get_session),
    redis: Redis = Depends(get_redis),
):
    ins = await services.company.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if await services.company.check_name_exists(db, name=model.name, ins=ins):
        raise exceptions.ExistsError()

    await services.company.edit(db, ins=ins, model=model, redis=redis)
    db.commit()
    return dict(msg="操作成功")


@router.put(
    "/delete/<int:pk>",
    summary="删除企业",
    response_model=schemas.Msg,
)
async def delete(
    pk: int,
    db: Session = Depends(get_session),
    redis: Redis = Depends(get_redis),
):
    ins = await services.company.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if ins.status == 1:
        raise exceptions.ValidateError("企业状态已变更, 请刷新后重试.")

    await services.company.delete(db, ins=ins, redis=redis)
    db.commit()
    return dict(msg="操作成功")


@router.get(
    "/option",
    summary="企业下拉框",
    response_model=List[schemas.CompanyOption],
)
async def option(
    keyword: str = None,
    db: Session = Depends(get_session),
):
    result = await services.company.get_filter(db, keyword=keyword)
    return result.all()
