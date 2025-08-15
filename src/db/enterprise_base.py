from functools import cached_property
from typing import TypeVar, Type, Any

from sqlalchemy import ForeignKey, and_, or_, select, Boolean, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, Load

from src.db import get_session
from src.db.base import Base
from src.db.utils import orm

T = TypeVar('T', bound='BaseModel')


class EnterpriseGeneralBase(Base):
    __abstract__ = True

    enterprise_id: Mapped[int] = mapped_column(
        ForeignKey(
            'enterprise.id',
            ondelete='CASCADE'
        ),
        nullable=True
    )
    is_general: Mapped[bool] = mapped_column(Boolean, default=False)

    @classmethod
    def field_name(cls: Type[T]) -> str:
        raise NotImplementedError

    @classmethod
    async def exists_value_with_session(
            cls: Type[T],
            session: AsyncSession,
            value: Any,
            enterprise_id: int
    ) -> bool:
        field = getattr(cls, cls.field_name())  # например, cls.name
        stmt = select(
            exists().where(
                or_(
                    and_(cls.enterprise_id == enterprise_id, cls.is_general.is_(False), field == value),
                    and_(cls.enterprise_id is None, cls.is_general.is_(True), field == value)
                )
            )
        )
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_by_enterprise(
            cls: Type[T],
            id_: int,
            enterprise_id: int,
            load_options: list[Load] | None = None,
    ) -> T | None:
        async with get_session() as session:
            # запрос при котором либо общие данные, либо те которые есть у компании
            stmt = (
                select(cls)
                .where(
                    or_(
                        and_(
                            cls.is_general.is_(False),
                            cls.id == id_,
                            cls.enterprise_id == enterprise_id,
                        ),
                        and_(
                            cls.id == id_,
                            cls.is_general.is_(True)
                        )
                    )
                )
            )
            # прикручиваем зависимости load options
            stmt = orm.apply_load_options(stmt, load_options)

            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def create_by_enterprise(
            cls: Type[T],
            enterprise_id: int,
            **kwargs: Any
    ) -> T:
        if enterprise_id is None:
            raise ValueError('enterprise_id is required')
        if kwargs.get('is_general'):
            raise ValueError('is_general is not used')
        # ВАЖНО: получаем имя поля и значение из kwargs
        field_name = cls.field_name()
        field_value = kwargs.get(field_name)
        if field_value is None:
            raise ValueError(f"{field_name} is required for uniqueness check")

        async with get_session() as session:
            if await cls.exists_value_with_session(session, field_value, enterprise_id):
                raise ValueError(f'object is already exists')
            return await cls.create_with_session(
                session,
                enterprise_id=enterprise_id,
                is_general=False,
                **kwargs
            )

    @classmethod
    async def delete_by_enterprise(
            cls: Type[T],
            id_: int,
            enterprise_id: int
    ) -> bool:
        """
                удаление модели, причём нельзя удалять чужие модели или общие
                :param id_: id модели который хотим поменять
                :param enterprise_id: id компании
                :return: boolean - удалена модель или нет
        """
        async with get_session() as session:
            stmt = (
                select(cls)
                .where(
                    and_(
                        cls.enterprise_id == enterprise_id,
                        cls.id == id_,
                        cls.is_general.is_(False)
                    )
                )
            )
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if not obj:
                raise ValueError(f'enterprise {enterprise_id} not found')
            await obj.delete_with_session(session)
        return True

    @classmethod
    async def update_by_enterprise(
            cls: Type[T],
            id_: int,
            enterprise_id: int,
            **kwargs
    ) -> T:
        """
        update модели, причём нельзя менять чужие модели или общие
        :param id_: id модели который хотим поменять
        :param enterprise_id: id компании
        :param kwargs: переменные модели
        :return: новая модель с полями
        """
        async with get_session() as session:
            if kwargs.get('is_general') or kwargs.get('enterprise_id'):
                raise ValueError("Invalid fields")
            stmt = (
                select(cls)
                .where(
                    and_(
                        cls.id == id_,
                        cls.enterprise_id == enterprise_id,
                        cls.is_general.is_(False)
                    )
                )
            )
            result = await session.execute(stmt)
            obj = result.scalar_one_or_none()
            if not obj:
                raise ValueError("Not found")
            await obj.update_with_session(session, **kwargs)
            return obj

    @classmethod
    async def list_by_enterprise(
            cls: Type[T],
            enterprise_id: int,
            load_options: list[Load] | None = None,
            **kwargs: Any
    ) -> list[T]:
        async with get_session() as session:
            # Общие фильтры из kwargs
            filters_from_kwargs = orm.build_filters(cls, kwargs)
            stmt = select(cls).where(
                or_(
                    and_([
                        cls.is_general.is_(False),
                        cls.enterprise_id == enterprise_id,
                        *filters_from_kwargs
                    ]),
                    and_([
                        cls.is_general.is_(True),
                        *filters_from_kwargs
                    ])
                )
            )
            # прикручиваем зависимости load options
            stmt = orm.apply_load_options(stmt, load_options)

            result = await session.execute(stmt)
            return result.scalars().all()


class EnterpriseBase(Base):
    __abstract__ = True

    enterprise_id: Mapped[int] = mapped_column(
        ForeignKey(
            'enterprise.id',
            ondelete='CASCADE'
        ),
        nullable=False
    )

    @classmethod
    async def get_by_enterprise_with_session(
            cls: Type[T],
            id_: int,
            enterprise_id: int,
            session: AsyncSession,
            load_options: list[Load] | None = None,
            **kwargs: Any
    ) -> T | None:
        print("get enterprise id:",  enterprise_id)
        stmt = (
            select(cls)
            .where(
                and_(
                    cls.enterprise_id == enterprise_id,
                    cls.id == id_,
                )
            )
        )
        # Добавляем фильтры по полям, которые есть в модели и переданы в kwargs
        filters = orm.build_filters(cls, {k: v for k, v in kwargs.items() if v is not None})
        if filters:
            stmt = stmt.where(*filters)
        # прикручиваем зависимости load options
        stmt = orm.apply_load_options(stmt, load_options)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_enterprise(
            cls: Type[T],
            id_: int,
            enterprise_id: int,
            load_options: list[Load] | None = None,
            **kwargs: Any
    ) -> T | None:
        async with get_session() as session:
            return await cls.get_by_enterprise_with_session(
                id_, enterprise_id, session, load_options, **kwargs
            )

    @classmethod
    async def create_by_enterprise(
            cls: Type[T],
            enterprise_id: int,
            load_options: list[Load] | None = None,
            **kwargs: Any
    ) -> T:
        if enterprise_id is None:
            raise ValueError('enterprise_id is required')
        async with get_session() as session:
            obj = await cls.create_with_session(
                session,
                enterprise_id=enterprise_id,
                **kwargs
            )
            if load_options:
                return await cls.get_by_enterprise_with_session(
                    obj.id, enterprise_id, session, load_options
                )
            return obj

    @classmethod
    async def delete_by_enterprise(
            cls: Type[T],
            id_: int,
            enterprise_id: int
    ) -> bool:
        obj = await cls.get_by_enterprise(id_, enterprise_id)
        if not obj:
            raise ValueError('object not found')
        return await obj.delete()

    @classmethod
    async def update_by_enterprise(
            cls: Type[T],
            id_: int,
            enterprise_id: int,
            load_options: list[Load] | None = None,
            **kwargs
    ) -> T:
        print(enterprise_id)
        async with get_session() as session:
            obj = await cls.get_by_enterprise_with_session(
                id_, enterprise_id, session, load_options
            )
            print(obj)
            if not obj:
                raise ValueError('enterprise not found')
            updated = await obj.update_with_session(session, **kwargs)
            if load_options:
                return await cls.get_by_enterprise_with_session(
                    updated.id, enterprise_id, session, load_options, **kwargs
                )
            return updated

    @classmethod
    async def list_by_enterprise(
            cls: Type[T],
            enterprise_id: int,
            load_options: list[Load] | None = None,
            **kwargs: Any,
    ) -> list[T]:
        async with get_session() as session:
            # Начинаем с базового запроса
            stmt = select(cls).where(cls.enterprise_id == enterprise_id)
            # Добавляем фильтры по полям, которые есть в модели и переданы в kwargs
            filters = orm.build_filters(cls, kwargs)
            if filters:
                stmt = stmt.where(*filters)
            # прикручиваем зависимости load options
            stmt = orm.apply_load_options(stmt, load_options)

            result = await session.execute(stmt)
            return result.scalars().all()
