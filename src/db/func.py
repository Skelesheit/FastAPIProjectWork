from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from src.db import db
from src.db.db_boundary import translate_db_errors, CONSTRAINT_MAP


async def get_session() -> AsyncIterator[AsyncSession]:
    """
    Хендлер транзакции (не сессии)
    Без обработки ошибок
    :return: Транзакция -> sqlalchemy.orm. AsyncSession
    """
    async with db.AsyncSessionLocal() as session:
        async with session.begin():
            yield session


async def get_session_tx() -> AsyncIterator[AsyncSession]:
    """
    Хендлер транзакции (не сессии)
    Главная особенность - обрабатывает SQL исключения
    Маппинг SQL исключений в сервисные исключения
    :return: Транзакция -> sqlalchemy.orm. AsyncSession
    """
    async with db.AsyncSessionLocal() as session:
        # ВНЕШНЯЯ рамка: перевод SQL-исключений в сервисные
        async with translate_db_errors(
                constraint_map=CONSTRAINT_MAP,
                debug_details=settings.BACKEND_DEBUG
        ):
            # ВНУТРЕННЯЯ рамка: одна транзакция на весь хендлер
            async with session.begin():
                yield session

async def get_session_raw() -> AsyncIterator[AsyncSession]:
    """
    Хендлер для создания сессии
    :return:
    """
    async with db.AsyncSessionLocal() as session:
        yield session