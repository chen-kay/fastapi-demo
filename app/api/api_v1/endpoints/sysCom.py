from app import schemas
from app.core import exceptions
from app.services import CompanyService, UserService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/",
    summary="获取企业列表",
    response_model=schemas.Pageination[schemas.CompanyType],
)
async def list(
    page: int = 1,
    limit: int = 10,
    company_service: CompanyService = Depends(CompanyService),
):
    result, total = await company_service.get_list(
        page=page,
        limit=limit,
    )
    return dict(data=result, total=total)


@router.post(
    "/add",
    summary="新增企业",
    response_model=schemas.Msg,
)
async def add(
    model: schemas.CompanyAdd,
    company_service: CompanyService = Depends(CompanyService),
    user_service: UserService = Depends(UserService),
):
    if await company_service.check_code_exists(model.code):
        raise exceptions.ExistsError()
    if await company_service.check_name_exists(model.name):
        raise exceptions.ExistsError()

    ins = await company_service.add(model)
    # 创建管理员账户
    await user_service.create_admin_user(ins)
    return dict(msg="操作成功")


@router.put(
    "/edit/<int:pk>",
    summary="修改企业",
    response_model=schemas.Msg,
)
async def edit(
    pk: int,
    model: schemas.CompanyEdit,
    company_service: CompanyService = Depends(CompanyService),
):
    ins = await company_service.get_by_id(pk)
    if not ins:
        raise exceptions.NotFoundError()
    if await company_service.check_name_exists(model.name):
        raise exceptions.ExistsError()

    await company_service.edit(ins, model=model)
    return dict(msg="操作成功")


@router.delete(
    "/delete/<int:pk>",
    summary="删除企业",
    response_model=schemas.Msg,
)
async def delete(
    pk: int,
    company_service: CompanyService = Depends(CompanyService),
):
    ins = await company_service.get_by_id(pk)
    if not ins:
        raise exceptions.NotFoundError()

    await company_service.delete(ins)
    return dict(msg="操作成功")
