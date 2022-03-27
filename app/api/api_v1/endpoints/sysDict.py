from typing import List

from app import schemas
from app.api import auth
from app.services import DictService, UserService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", summary="获取字典列表", response_model=List[schemas.DictType])
async def sysDictList(
    dict_service: DictService = Depends(DictService),
):
    result = await dict_service.get_dictionary_list()
    return result


@router.post(
    "/value",
    summary="获取字典值列表",
    response_model=schemas.Pageination[schemas.DictValueType],
)
async def sysDictValueList(
    parent_id: int,
    company_id: int = None,
    page: int = 1,
    limit: int = 10,
    user_service: UserService = Depends(UserService),
    dict_service: DictService = Depends(DictService),
    current: schemas.UserModel = Depends(auth.get_current_active_user),
):
    company_id = None
    if not user_service.is_superuser(current):
        company_id = company_id
    else:
        company_id = company_id
    result, total = await dict_service.get_dictvalue_list(
        parent_id=parent_id,
        company_id=company_id,
        page=page,
        limit=limit,
    )
    return dict(data=result, total=total)
