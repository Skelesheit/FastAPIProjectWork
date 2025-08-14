# tests/conftest.py
import asyncio
import os
import pytest
from typing import AsyncIterator, Callable, Awaitable
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import event
from httpx import AsyncClient

from config import settings

# важно: укажи тестовый DSN (ОТДЕЛЬНАЯ БД!)
TEST_DB_DSN = settings.db_orm_url

# импортируем твой FastAPI app и зависимости
from main import app  # где ты регаешь exception handlers и роуты
from src.db.func import get_session_tx  # твоя DI-зависимость
from src.db.base import Base  # где metadata всех моделей
from src.clients import captcha, mail

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def engine():
    eng = create_async_engine(TEST_DB_DSN, pool_pre_ping=True)
    async with eng.begin() as conn:
        # если не через alembic — создаём схему
        await conn.run_sync(Base.metadata.create_all)
    yield eng
    await eng.dispose()

@pytest.fixture
async def session_factory(engine) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    SessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    yield SessionLocal

@pytest.fixture
async def db_session(session_factory) -> AsyncIterator[AsyncSession]:
    """
    Даёт один AsyncSession + SAVEPOINT на каждый тест.
    Любые коммиты внутри кода не уничтожат внешнюю транзакцию — мы её откатим.
    """
    async with session_factory() as session:
        # начинаем внешнюю транзакцию
        async with session.begin():
            # делаем savepoint (nested) — коммиты внутри кода не закроют внешнюю транзу
            nested = await session.begin_nested()

            # автоперезапуск savepoint'а после каждого внутреннего коммита
            @event.listens_for(session.sync_session, "after_transaction_end")
            def _restart_savepoint(sess, trans):
                if trans.nested and not trans._parent.nested:
                    sess.begin_nested()

            yield session

            # откатываем всё, что сделал тест
            await nested.rollback()

@pytest.fixture
async def app_with_overrides(db_session) -> AsyncIterator:
    """
    Подменяем DI: get_session_tx -> отдаём наш тестовый session
    """
    async def _override_dep() -> AsyncIterator[AsyncSession]:
        # тут НЕ открываем begin(): у нас уже есть внешняя транзакция + savepoint
        yield db_session

    app.dependency_overrides[get_session_tx] = _override_dep
    # при желании можно ещё подменить другие зависимости (например, current_user)
    yield app
    app.dependency_overrides.clear()

@pytest.fixture
async def client(app_with_overrides) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(app=app_with_overrides, base_url="http://test") as ac:
        yield ac

# моки капчи и почты
@pytest.fixture(autouse=True)
def mock_captcha_mail(monkeypatch):
    async def _captcha_ok(token: str, ip: str) -> bool:
        return True
    monkeypatch.setattr(captcha, "verify_yandex_captcha", _captcha_ok)

    async def _send_registration_email(user_id: int, email: str):
        # no-op
        return None
    monkeypatch.setattr(mail, "send_registration_email", _send_registration_email)
