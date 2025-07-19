import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import settings

# Создание асинхронного движка
async_engine = create_async_engine(settings.db_orm_url, echo=True)

# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

session = AsyncSessionLocal()


# Пример использования сессии
async def test_connection():
    async with async_engine.connect() as conn:
        await conn.execute("SELECT 1")
        print("Connected to database lol")


if __name__ == "__main__":
    asyncio.run(test_connection())
