from app import schemas
from app.core.config import settings
from app.core.logger import logger
from app.services import UserService
from sqlalchemy.orm import Session


async def init_db(db: Session) -> None:
    # Base.metadata.create_all(bind=engine)

    user_service = UserService(db)
    logger.info("Creating Admin User")
    user = await user_service.get_by_username(settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserAdd(
            username=settings.FIRST_SUPERUSER,
            fullname=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
        )
        user = await user_service.add(user_in, is_superuser=1)
