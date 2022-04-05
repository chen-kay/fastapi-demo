from app import schemas, services
from app.core.config import settings
from app.core.logger import logger
from sqlalchemy.orm import Session


async def init_db(db: Session) -> None:
    logger.info("Creating Super User")
    user_name = f"{settings.FIRST_SUPERUSER}@{settings.FIRST_SUPERDOMAIN}"
    user = await services.user.get_by_user_name(db, user_name=user_name)
    if not user:
        user_in = schemas.UserAdd(
            username=settings.FIRST_SUPERUSER,
            fullname=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = await services.user.add(
            db,
            model=user_in,
            is_superuser=1,
            is_admin=1,
            user_name=user_name,
        )
        db.commit()
