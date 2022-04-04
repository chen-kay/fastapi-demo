from typing import List

from aioredis import Redis
from app import schemas, services
from app.api.deps import get_current_active_user
from app.core import exceptions
from app.db.deps import get_redis, get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/",
    summary="获取组织列表",
    response_model=schemas.Pageination[schemas.OrgType],
)
async def list(
    filters: schemas.OrgQuery = Depends(),
    db: Session = Depends(get_session),
    redis: Redis = Depends(get_redis),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    company_id = filters.company_id
    parent_ids = None
    if not services.user.is_superuser(current):
        company_id = current.company_id
    org_data = await services.org.get_org_data(db, company_id=company_id, redis=redis)
    if filters.parent_id:
        parent_ids = services.org.get_sub_org_ids(filters.parent_id, org_data)
    qs = await services.org.get_list(
        db,
        company_id=company_id,
        parent_id=filters.parent_id,
        parent_ids=parent_ids,
        name=filters.name,
        keyword=filters.keyword,
    )
    result, total = services.org.get_pagination(
        qs,
        page=filters.page,
        limit=filters.page_size,
    )
    data = services.org.get_list_data(result, org_data=org_data)
    return dict(data=data, total=total)


@router.post(
    "/add",
    summary="新增组织",
    response_model=schemas.Msg,
)
async def add(
    model: schemas.OrgAdd,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    if await services.org.check_code_exists(db, code=model.code):
        raise exceptions.ExistsError("新增失败: 组织机构编码重复, 请检查code参数")
    if await services.org.check_name_exists(db, name=model.name):
        raise exceptions.ExistsError("新增失败: 组织机构名称重复, 请检查name参数")

    if not services.user.is_superuser(current):
        model.company_id = current.company_id
    await services.org.add(db, model=model)
    db.commit()
    return dict(msg="操作成功")


@router.put(
    "/edit/<int:pk>",
    summary="修改组织",
    response_model=schemas.Msg,
)
async def edit(
    pk: int,
    model: schemas.OrgEdit,
    db: Session = Depends(get_session),
    redis: Redis = Depends(get_redis),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    ins = await services.org.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if not await services.user.check_user_company(current, ins.company_id):
        raise exceptions.NotFoundError()

    data = await services.org.get_org_data(db, company_id=ins.company_id, redis=redis)
    parent_ids = services.org.get_parent_ids(model.parent_id, data)
    if ins.id == model.parent_id:
        raise exceptions.ValidateError("编辑失败：父节点不能和本节点一致，请重新选择父节点")
    if ins.id in parent_ids:
        raise exceptions.ValidateError("编辑失败: 父节点不能为本节点的子节点, 请重新选择父节点")
    if await services.org.check_code_exists(db, code=model.code, ins=ins):
        raise exceptions.ExistsError("编辑失败: 组织机构编码重复, 请检查code参数")
    if await services.org.check_name_exists(db, name=model.name, ins=ins):
        raise exceptions.ExistsError("编辑失败: 组织机构名称重复, 请检查name参数")

    await services.org.edit(db, ins=ins, model=model)
    db.commit()
    return dict(msg="操作成功")


@router.delete(
    "/delete/<int:pk>",
    summary="删除组织",
    response_model=schemas.Msg,
)
async def delete(
    pk: int,
    db: Session = Depends(get_session),
    redis: Redis = Depends(get_redis),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    ins = await services.org.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if not await services.user.check_user_company(current, ins.company_id):
        raise exceptions.NotFoundError()
    org_data = await services.org.get_org_data(
        db,
        company_id=ins.company_id,
        redis=redis,
    )
    parent_ids = services.org.get_sub_org_ids(ins.id, org_data)
    if await services.org.check_user_exists(db, org_ids=parent_ids):
        raise exceptions.ValidateError("删除失败: 该机构或子机构下有员工, 无法删除")

    await services.org.delete(db, ins=ins, redis=redis)
    db.commit()
    return dict(msg="操作成功")


@router.get(
    "/tree",
    summary="组织树",
    response_model=List[schemas.OrgTree],
)
async def tree(
    company_id: int = None,
    db: Session = Depends(get_session),
):
    data = await services.org.get_org_data(db, company_id=company_id)
    return services.org.get_tree_data(data)
