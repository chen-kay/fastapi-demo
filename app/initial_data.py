import asyncio
import sys
from pathlib import Path

sys_dir = Path("..")
sys.path.append(str(sys_dir.cwd()))

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.session import SessionLocal
from app.schemas.models.user import UserCreate
from app.services.user import UserService

user_list = [
    {
        "user_name": "admin",
        "username": "admin",
        "fullname": "admin",
        "password": "admin",
    },
]


async def init_db(session: Session) -> None:
    user_service = UserService(session)
    for user in user_list:
        model = UserCreate(**user)
        ins = await user_service.get_by_user_name(model.user_name)
        if ins:
            continue
        await user_service.create_superuser(model=model)


async def init() -> None:
    session = SessionLocal()
    await init_db(session)


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
