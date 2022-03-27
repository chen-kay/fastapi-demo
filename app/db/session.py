from app.core.config import settings
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)
