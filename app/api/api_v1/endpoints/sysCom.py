from typing import List

from aioredis import Redis
from app import schemas, services
from app.api import deps
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
        raise exceptions.ExistsError("新增失败: 企业域名重复, 请检查domain参数")
    if await services.company.check_name_exists(db, name=model.name):
        raise exceptions.ExistsError("新增失败: 企业名称重复, 请检查name参数")

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
        raise exceptions.ExistsError("编辑失败: 企业名称重复, 请检查name参数")

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
        raise exceptions.ValidateError("新增失败: 企业必须已禁用或已过期, 请检查企业状态")

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


@router.put(
    "/switch/<int:pk>",
    summary="切换企业",
    response_model=List[schemas.Msg],
)
async def option(
    pk: int,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(deps.get_current_active_superuser),
):
    ins = await services.company.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    await services.user.switch_company(db, ins=current, company_id=pk)
    db.commit()
    return dict(msg="操作成功")
