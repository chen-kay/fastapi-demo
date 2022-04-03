from typing import List

from app import schemas, services
from app.db.deps import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", summary="获取字典列表", response_model=List[schemas.DictTypeType])
async def sysDictList(
    db: Session = Depends(get_session),
):
    result = await services.dict_type.get_list(db)
    return result
