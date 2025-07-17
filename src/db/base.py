from typing import TypeVar, Type, Any, ClassVar

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, InstrumentedAttribute

from src.db import get_session

T = TypeVar('T', bound='BaseModel')


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @classmethod
    async def get_by_id(cls: Type[T], id_: int) -> T | None:
        async with get_session() as session:
            stmt = select(cls).where(cls.id == id_)
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
        return obj

    @classmethod
    async def create(cls: Type[T], **kwargs: Any) -> T:
        async with get_session() as session:
            obj = cls(**kwargs)
            session.add(obj)
            await session.flush()
            await session.refresh(obj)
        return obj

    @classmethod
    async def delete(cls: Type[T]) -> None:
        async with get_session() as session:
            await session.execute(delete(cls))

    async def update(self, **kwargs) -> None:
        async with get_session() as session:
            stmt = update(type(self)).where(type(self).id == self.id).values(**kwargs)
            await session.execute(stmt)
            await session.flush()
            await session.refresh(self)
