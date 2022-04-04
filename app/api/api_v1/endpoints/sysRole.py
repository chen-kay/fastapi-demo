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
    summary="获取角色列表",
    response_model=schemas.Pageination[schemas.RoleType],
)
async def list(
    filters: schemas.RoleQuery = Depends(),
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    company_id = filters.company_id
    if not services.user.is_superuser(current):
        company_id = current.company_id
    qs = await services.role.get_list(
        db,
        company_id=company_id,
        name=filters.name,
        keyword=filters.keyword,
    )
    result, total = services.role.get_pagination(
        qs,
        page=filters.page,
        limit=filters.page_size,
    )
    return dict(data=result, total=total)


@router.post(
    "/add",
    summary="新增角色",
    response_model=schemas.Msg,
)
async def add(
    model: schemas.RoleAdd,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    if await services.role.check_code_exists(db, code=model.code):
        raise exceptions.ExistsError("新增失败: 角色机构编码重复, 请检查code参数")
    if await services.role.check_name_exists(db, name=model.name):
        raise exceptions.ExistsError("新增失败: 角色机构名称重复, 请检查name参数")

    if not services.user.is_superuser(current):
        model.company_id = current.company_id
    await services.role.add(db, model=model)
    db.commit()
    return dict(msg="操作成功")


@router.put(
    "/edit/<int:pk>",
    summary="修改角色",
    response_model=schemas.Msg,
)
async def edit(
    pk: int,
    model: schemas.RoleEdit,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    ins = await services.role.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if not await services.user.check_user_company(current, ins.company_id):
        raise exceptions.NotFoundError()
    if await services.role.check_code_exists(db, code=model.code, ins=ins):
        raise exceptions.ExistsError("编辑失败: 角色编码重复, 请检查code参数")
    if await services.role.check_name_exists(db, name=model.name, ins=ins):
        raise exceptions.ExistsError("编辑失败: 角色名称重复, 请检查name参数")

    await services.role.edit(db, ins=ins, model=model)
    db.commit()
    return dict(msg="操作成功")


@router.delete(
    "/delete/<int:pk>",
    summary="删除角色",
    response_model=schemas.Msg,
)
async def delete(
    pk: int,
    db: Session = Depends(get_session),
    redis: Redis = Depends(get_redis),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    ins = await services.role.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if not await services.user.check_user_company(current, ins.company_id):
        raise exceptions.NotFoundError()
    if await services.role.check_user_exists(db, role_id=ins.id):
        raise exceptions.ValidateError("删除失败: 该角色下有员工, 无法删除")

    await services.role.delete(db, ins=ins, redis=redis)
    db.commit()
    return dict(msg="操作成功")


@router.put(
    "/grantMenu",
    summary="授权菜单",
    response_model=schemas.Msg,
)
async def grantMenu(
    pk: int,
    model: schemas.RoleGrantMenu,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    ins = await services.role.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if not await services.user.check_user_company(current, ins.company_id):
        raise exceptions.NotFoundError()

    access = await services.access.get_list(db, ids=model.access_ids)
    ins.access = access.all()
    await services.role.grant_menu(db, model=model)
    db.commit()
    return dict(msg="操作成功")


@router.put(
    "/grantData",
    summary="授权数据",
    response_model=schemas.Msg,
)
async def grantData(
    pk: int,
    model: schemas.RoleGrantData,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    ins = await services.role.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if not await services.user.check_user_company(current, ins.company_id):
        raise exceptions.NotFoundError()

    orgs = await services.org.get_list(db, company_id=ins.company_id, ids=model.org_ids)
    ins.orgs = orgs.all()
    await services.role.grant_data(db, ins=ins, model=model)
    db.commit()
    return dict(msg="操作成功")


@router.get(
    "/ownMenu",
    summary="已授权菜单",
    response_model=schemas.RoleOwnMenu,
)
async def ownMenu(
    pk: int,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    ins = await services.role.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if not await services.user.check_user_company(current, ins.company_id):
        raise exceptions.NotFoundError()

    ins.access_ids = [r.id for r in ins.access]
    return ins


@router.get(
    "/ownData",
    summary="已授权数据",
    response_model=schemas.RoleOwnData,
)
async def ownData(
    pk: int,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(get_current_active_user),
):
    ins = await services.role.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if not await services.user.check_user_company(current, ins.company_id):
        raise exceptions.NotFoundError()

    ins.org_ids = [r.id for r in ins.orgs]
    return ins
