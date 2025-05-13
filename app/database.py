from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from enum import Enum

from app.config import config as conf

# создаём движок и фабрику сессий
engine = create_async_engine(conf.database_url, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_session() -> AsyncSession:
    """
    Asynchronous context manager for SQLAlchemy sessions.
    Использование:
        async with get_session() as session:
            ...
    """
    async with async_session() as session:
        yield session

class Base(DeclarativeBase):
    pass

class BaseEnum(Enum):
    @classmethod
    async def list_values(cls):
        return [member.value for member in cls]
