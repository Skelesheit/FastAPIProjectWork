from typing import TypeVar, Type, Any, List

from sqlalchemy import update, select, and_
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.db import get_session

T = TypeVar('T', bound='Base')


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @classmethod
    async def get_with_session(
            cls: Type[T],
            session: AsyncSession,
            id_: int
    ) -> T | None:
        stmt = select(cls).where(cls.id == id_)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get(cls: Type[T], id_: int) -> T | None:
        async with get_session() as session:
            return await cls.get_with_session(id_, session)

    @classmethod
    async def create(cls: Type[T], **kwargs: Any) -> T:
        async with get_session() as session:
            return await cls.create_with_session(session, **kwargs)

    @classmethod
    async def create_with_session(
            cls: Type[T],
            session: AsyncSession,
            **kwargs: Any
    ) -> T:
        obj = cls(**kwargs)
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    async def delete_with_session(self: T, session: AsyncSession) -> bool:
        await session.delete(self)
        await session.flush()
        return True

    async def delete(self: T) -> bool:
        """
        Вот тут немного не знаю как правильно
        проверить без ещё одного запроса лишнего
        :return: True
        """
        async with get_session() as session:
            await self.delete_with_session(session)
        return True

    async def update_with_session(
            self: T,
            session: AsyncSession,
            **kwargs: Any
    ) -> T:
        stmt = (
            update(type(self))
            .where(type(self).id == self.id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        await session.execute(stmt)
        await session.flush()
        await session.refresh(self)
        return self

    async def update(self: T, **kwargs) -> T:
        async with get_session() as session:
            return await self.update_with_session(session, **kwargs)

    @classmethod
    async def list(cls: Type[T], **kwargs: Any) -> list[T]:
        async with get_session() as session:
            return await cls.list_with_session(session, **kwargs)

    @classmethod
    async def list_with_session(
            cls: Type[T],
            session: AsyncSession,
            **kwargs: Any
    ) -> List[T]:
        filters = list()
        for key, value in kwargs.items():
            if value is not None:
                filters.append(getattr(cls, key) == value)

        stmt = select(cls)
        if filters:
            stmt = stmt.where(and_(*filters))

        result = await session.execute(stmt)
        return list(result.scalars().all())
