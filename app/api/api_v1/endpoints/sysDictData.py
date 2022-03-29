from app import schemas
from app.api import auth
from app.core import exceptions
from app.services import DictDataService, DictTypeService, UserService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/",
    summary="获取字典值列表",
    response_model=schemas.Pageination[schemas.DictDataType],
)
async def list(
    parent_id: int,
    company_id: int = None,
    page: int = 1,
    limit: int = 10,
    user_service: UserService = Depends(UserService),
    dict_data_service: DictDataService = Depends(DictDataService),
    current: schemas.UserModel = Depends(auth.get_current_active_user),
):
    company_id = None
    if not user_service.is_superuser(current):
        company_id = company_id
    else:
        company_id = company_id
    result, total = await dict_data_service.get_list(
        parent_id=parent_id,
        company_id=company_id,
        page=page,
        limit=limit,
    )
    return dict(data=result, total=total)


@router.post(
    "/add",
    summary="新增字典值",
    response_model=schemas.Msg,
)
async def add(
    model: schemas.DictDataAdd,
    user_service: UserService = Depends(UserService),
    dict_data_service: DictDataService = Depends(DictDataService),
    dict_type_service: DictTypeService = Depends(DictTypeService),
    current: schemas.UserModel = Depends(auth.get_current_active_user),
):
    if not await dict_type_service.get_by_id(model.parent_id):
        raise exceptions.NotFoundError()
    if await dict_data_service.check_code_exists(model.code):
        raise exceptions.ExistsError()
    if await dict_data_service.check_value_exists(model.value):
        raise exceptions.ExistsError()
    if not user_service.is_superuser(current):
        model.company_id = current.company_id

    await dict_data_service.add(model)
    return dict(msg="操作成功")


@router.put(
    "/edit/<int:pk>",
    summary="修改字典值",
    response_model=schemas.Msg,
)
async def edit(
    pk: int,
    model: schemas.DictDataEdit,
    dict_data_service: DictDataService = Depends(DictDataService),
):
    ins = await dict_data_service.get_by_id(pk)
    if not ins:
        raise exceptions.NotFoundError()
    if await dict_data_service.check_code_exists(model.code, ins=ins):
        raise exceptions.ExistsError()
    if await dict_data_service.check_value_exists(model.value, ins=ins):
        raise exceptions.ExistsError()

    await dict_data_service.edit(ins, model=model)
    return dict(msg="操作成功")


@router.delete(
    "/delete/<int:pk>",
    summary="删除字典值",
    response_model=schemas.Msg,
)
async def delete(
    pk: int,
    dict_data_service: DictDataService = Depends(DictDataService),
):
    ins = await dict_data_service.get_by_id(pk)
    if not ins:
        raise exceptions.NotFoundError()

    await dict_data_service.delete(ins)
    return dict(msg="操作成功")
