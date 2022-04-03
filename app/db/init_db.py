from app import schemas
from app.core.config import settings
from app.core.logger import logger
from app.services import UserService
from sqlalchemy.orm import Session


async def init_db(db: Session) -> None:
    logger.info("Creating Super User")
    user_service = UserService(db)
    user_name = f"{settings.FIRST_SUPERUSER}@{settings.FIRST_SUPERDOMAIN}"
    user = await user_service.get_by_user_name(user_name)
    if not user:
        user_in = schemas.UserAdd(
            username=settings.FIRST_SUPERUSER,
            fullname=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = await user_service.add(
            user_in,
            is_superuser=1,
            user_name=user_name,
        )
