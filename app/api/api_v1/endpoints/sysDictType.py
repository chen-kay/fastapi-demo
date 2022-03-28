from typing import List

from app import schemas
from app.services import DictTypeService
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", summary="获取字典列表", response_model=List[schemas.DictTypeType])
async def sysDictList(
    dict_type_service: DictTypeService = Depends(DictTypeService),
):
    result = await dict_type_service.get_list()
    return result
