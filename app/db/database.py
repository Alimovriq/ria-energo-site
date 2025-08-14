from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.db.config import settings


engine = create_async_engine(settings.POSTGRES_URL, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> AsyncGenerator:
    """
    Асинхронное подключение к БД через контекстный менеджер
    :return: асинхронная сессия подключения
    """

    async with async_session() as session:
        yield session