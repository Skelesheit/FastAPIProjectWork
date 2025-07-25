from typing import TypeVar, Type, Any

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.db import get_session

T = TypeVar('T', bound='BaseModel')


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @classmethod
    async def get_with_session(cls: Type[T], session: AsyncSession, id_: int) -> T | None:
        stmt = select(cls).where(cls.id == id_)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get(cls: Type[T], id_: int) -> T | None:
        async with get_session() as session:
            obj = await cls.get_with_session(id_, session)
        return obj

    @classmethod
    async def create(cls: Type[T], **kwargs: Any) -> T:
        async with get_session() as session:
            obj = await cls.create_with_session(session, **kwargs)
        return obj

    @classmethod
    async def create_with_session(cls: Type[T], session: AsyncSession, **kwargs: Any) -> T:
        obj = cls(**kwargs)
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    async def delete_with_session(self: T, session: AsyncSession) -> None:
        await session.delete(self)
        await session.flush()

    async def delete(self: T) -> None:
        async with get_session() as session:
            await self.delete_with_session(session)

    async def update_with_session(self, session: AsyncSession, **kwargs: Any) -> None:
        stmt = (
            update(type(self))
            .where(type(self).id == self.id)
            .values(**kwargs)
            .execution_options(synchronize_session='fetch')
        )
        await session.execute(stmt)
        await session.flush()
        await session.refresh(self)

    async def update(self, **kwargs) -> None:
        async with get_session() as session:
            await self.update_with_session(session, **kwargs)
