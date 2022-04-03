from typing import List

from app import schemas
from app.core import exceptions
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get(
    "/",
    summary="获取组织列表",
    response_model=schemas.Pageination[schemas.OrgType],
)
async def list(
    filters: schemas.OrgQuery = Depends(),
    control: OrgController = Depends(),
):
    result, total = await control.get_list(filters)
    return dict(data=result, total=total)


@router.post(
    "/add",
    summary="新增组织",
    response_model=schemas.Msg,
)
async def add(
    model: schemas.OrgAdd,
    control: OrgController = Depends(),
):
    await control.add(model)
    return dict(msg="操作成功")


@router.put(
    "/edit/<int:pk>",
    summary="修改组织",
    response_model=schemas.Msg,
)
async def edit(
    pk: int,
    model: schemas.OrgEdit,
    control: OrgController = Depends(),
):
    ins = await control.org.get_by_id(pk)
    if not ins:
        raise exceptions.NotFoundError()
    await control.edit(ins, model=model)
    return dict(msg="操作成功")


@router.delete(
    "/delete/<int:pk>",
    summary="删除组织",
    response_model=schemas.Msg,
)
async def delete(
    pk: int,
    control: OrgController = Depends(),
):
    ins = await control.org.get_by_id(pk)
    if not ins:
        raise exceptions.NotFoundError()

    await control.delete(ins)
    return dict(msg="操作成功")


@router.get(
    "/tree",
    summary="组织树",
    response_model=List[schemas.OrgTree],
)
async def tree(
    control: OrgController = Depends(),
):
    data = await control.get_tree_list()
    return data


@router.get(
    "/export",
    summary="导出组织列表",
    response_model=List[schemas.OrgType],
)
async def list(
    filters: schemas.OrgQuery,
    control: OrgController = Depends(),
):
    result = await control.export(filters)
    return result
