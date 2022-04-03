from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(engine, autocommit=False, autoflush=False)

Base = declarative_base()
