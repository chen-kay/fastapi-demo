import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).absolute().parent.parent))  # fix no module name

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models import *
from app.models import User


async def init():
    session: Session = SessionLocal()
    await init_db(session)


async def main():
    logger.info("Creating Initial Table")
    await init()
    logger.info("Initial Table Ended")


if __name__ == "__main__":
    asyncio.run(main())
