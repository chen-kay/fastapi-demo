from app import schemas, services
from app.api import deps
from app.core import exceptions
from app.db.deps import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/",
    summary="获取字典值列表",
    response_model=schemas.Pageination[schemas.DictDataType],
)
async def list(
    filters: schemas.DictDataFilter = Depends(),
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(deps.get_current_active_user),
):
    if not services.user.is_superuser(current):
        filters.company_id = current.company_id
    result, total = await services.dict_data.get_pagination(db, filters=filters)
    return dict(data=result, total=total)


@router.post(
    "/add",
    summary="新增字典值",
    response_model=schemas.Msg,
)
async def add(
    model: schemas.DictDataAdd,
    db: Session = Depends(get_session),
    current: schemas.UserModel = Depends(deps.get_current_active_user),
):
    if not await services.dict_type.get_by_id(db, id=model.parent_id):
        raise exceptions.NotFoundError()
    if await services.dict_data.check_code_exists(db, code=model.code):
        raise exceptions.ExistsError()
    if await services.dict_data.check_value_exists(db, value=model.value):
        raise exceptions.ExistsError()
    if not services.user.is_superuser(current):
        model.company_id = current.company_id

    await services.dict_data.add(db, model=model)
    db.commit()
    return dict(msg="操作成功")


@router.put(
    "/edit/<int:pk>",
    summary="修改字典值",
    response_model=schemas.Msg,
)
async def edit(
    pk: int,
    model: schemas.DictDataEdit,
    db: Session = Depends(get_session),
):
    ins = await services.dict_data.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()
    if await services.dict_data.check_code_exists(db, code=model.code, ins=ins):
        raise exceptions.ExistsError()
    if await services.dict_data.check_value_exists(db, value=model.value, ins=ins):
        raise exceptions.ExistsError()

    await services.dict_data.edit(db, ins=ins, model=model)
    db.commit()
    return dict(msg="操作成功")


@router.delete(
    "/delete/<int:pk>",
    summary="删除字典值",
    response_model=schemas.Msg,
)
async def delete(
    pk: int,
    db: Session = Depends(get_session),
):
    ins = await services.dict_data.get_by_id(db, id=pk)
    if not ins:
        raise exceptions.NotFoundError()

    await services.dict_data.delete(db, ins=ins)
    db.commit()
    return dict(msg="操作成功")
