import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))  # fix no module name
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from app.core.config import settings
from app.core.logger import logger
from app.core.security import get_password_hash
from app.db.session import SessionLocal, engine
from app.models import *
from app.models import User


def init_database():
    if not database_exists(settings.SQLALCHEMY_DATABASE_URL):
        create_database(settings.SQLALCHEMY_DATABASE_URL, encoding="utf8mb4")


async def init_admin(session: Session):
    admin = User(
        username=settings.ADMIN_USERNAME,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        nickname=settings.ADMIN_NICKNAME,
        email=settings.ADMIN_EMAIL,
        is_superuser=1,
    )
    session.add(admin)
    session.commit()


async def init_table():
    logger.info("Creating Initial Table")

    metadata = MetaData()
    logger.info("Droping Table")
    metadata.drop_all(engine)
    logger.info("Creating Table")
    metadata.create_all(engine)
    logger.info("Creating Admin User")
    await init_admin(SessionLocal())
    logger.info("Initial Table Ended")


if __name__ == "__main__":
    init_database()
    asyncio.run(init_table())
