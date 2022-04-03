from typing import List

from app import schemas
from app.controller import DictTypeController
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/", summary="获取字典列表", response_model=List[schemas.DictTypeType])
async def sysDictList(
    control: DictTypeController = Depends(),
):
    result = await control.get_list()
    return result
