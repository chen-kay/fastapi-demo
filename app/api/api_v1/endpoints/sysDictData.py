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
    qs = await services.dict_data.get_list(
        db,
        company_id=current.company_id,
        parent_id=filters.parent_id,
        keyword=filters.keyword,
    )
    result, total = services.dict_data.pagination(
        qs,
        page=filters.page,
        limit=filters.page_size,
    )
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
        raise exceptions.ExistsError("新增失败: 字典编码重复, 请检查code参数")
    if await services.dict_data.check_value_exists(db, value=model.value):
        raise exceptions.ExistsError("新增失败: 字典值重复, 请检查value参数")

    await services.dict_data.add(db, model=model, company_id=current.company_id)
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
    current: schemas.UserModel = Depends(deps.get_current_active_user),
):
    ins = await services.dict_data.get_by_id(db, id=pk, company_id=current.company_id)
    if not ins:
        raise exceptions.NotFoundError()
    if await services.dict_data.check_code_exists(db, code=model.code, ins=ins):
        raise exceptions.ExistsError("编辑失败: 字典编码重复, 请检查code参数")
    if await services.dict_data.check_value_exists(db, value=model.value, ins=ins):
        raise exceptions.ExistsError("编辑失败: 字典值重复, 请检查code参数")

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
    current: schemas.UserModel = Depends(deps.get_current_active_user),
):
    ins = await services.dict_data.get_by_id(db, id=pk, company_id=current.company_id)
    if not ins:
        raise exceptions.NotFoundError()

    await services.dict_data.delete(db, ins=ins)
    db.commit()
    return dict(msg="操作成功")
