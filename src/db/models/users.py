from __future__ import annotations

import secrets
from datetime import datetime, timedelta

from sqlalchemy import DateTime, Boolean, ForeignKey, String, func, exists
from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Mapped, mapped_column

from config import settings
from src.auth.hash import validate, hash_password
from src.db import get_session
from src.db.base import Base


class User(Base):
    __tablename__ = 'user'

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_member: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    token: Mapped['RefreshToken'] = relationship(
        'RefreshToken',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan'
    )

    enterprise_member: Mapped['EnterpriseMember'] = relationship(
        'EnterpriseMember',
        back_populates='user',
        uselist=False
    )

    @classmethod
    async def create(cls, email: str, password: str) -> User:
        """
        Регистрация пользователя
        :param email: email
        :param password: пароль
        :return: новый пользователь в системе User
        """
        async with get_session() as session:
            user = User(email=email, password=hash_password(password))
            session.add(user)
            await session.flush()
            await session.refresh(user)
        return user

    @classmethod
    async def verify_email(cls, user_id: int) -> bool:
        """
        Делаем пользователя верифицированным (is_verify = True)
        :param user_id: int
        :return: bool - выполнился запрос или нет
        """
        async with get_session() as session:
            stmt = (
                update(cls)
                .where(cls.id == user_id)
                .values(is_verified=True)
                .execution_options(synchronize_session='evaluate')
            )
            result = await session.execute(stmt)
        return result.rowcount > 0

    @classmethod
    async def has_email(cls, email: str) -> bool:
        """
        Метод для проверки email в базе данных (есть ли такой email в БД)
        :param email: значение email
        :return: bool
        """
        async with get_session() as session:
            stmt = select(exists().where(cls.email == email))
            result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_by_email(cls, email: str) -> User | None:
        """
        Взятие User по email
        :param email: значение
        :return: ORM User
        """
        async with get_session() as session:
            stmt = select(cls).where(cls.email == email)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_email_with_session(cls, session: AsyncSession,  email: str) -> User | None:
        """
        Взятие User по email: версия с открытой сессией
        :param session: асинхронная сессия
        :param email: email сотрудника
        :return: User ORM
        """
        stmt = select(cls).where(cls.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


    @classmethod
    async def get_all_data(cls, id_: int) -> User | None:
        """
        Все данные об пользователе (компания, пользователь, сотрудник)
        ПЕРЕДЕЛАТЬ МЕТОД!!!
        :param id_: id сотрудника
        :return: вся информация об пользователе
        """
        async with get_session() as session:
            stmt = select(cls).where(cls.id == id_)
            result = await session.execute(stmt)
        return result.scalars().one_or_none()

    def check_password(self, password: str) -> bool:
        """
        Проверка пароля для входа в аккаунт
        :param password: значение пароля
        :return: bool
        """
        return validate(password, self.password)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


class RefreshToken(Base):
    __tablename__ = 'token'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped['User'] = relationship(
        'User',
        back_populates='token',
        uselist=False
    )

    @property
    def expired(self) -> bool:
        """
        Истёк ли токен?
        :return: bool
        """
        return self.expires_at < datetime.now()

    @classmethod
    async def get_by_token(cls, token: str) -> RefreshToken | None:
        """
        Находим модель токена по значению
        :param token: значение токена
        :return: токен или None
        """
        async with get_session() as session:
            stmt = select(cls).where(cls.token == token)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def delete_by_token(cls, token: str) -> None:
        """
        Удаляет старый токен при помощи значения
        :param token: значение токена
        :return: None
        """
        async with get_session() as session:
            stmt = delete(cls).where(cls.token == token)
            await session.execute(stmt)

    @classmethod
    async def create(cls, user_id: int) -> RefreshToken:
        """
        Удаляет старый токен и создаёт новый
        :param user_id: id Пользователя, владельца токена
        :return: model RefreshToken
        """
        await cls.delete_by_user_id(user_id)
        token = secrets.token_urlsafe(64)
        expires = datetime.now() + timedelta(days=settings.EXPIRES_REFRESH_TOKEN_DAYS)
        async with get_session() as session:
            refresh_token = RefreshToken(
                user_id=user_id,
                token=token,
                expires_at=expires
            )
            session.add(refresh_token)
            await session.flush()
            await session.refresh(refresh_token)
        return refresh_token

    @classmethod
    async def delete_by_user_id(cls, user_id: int) -> None:
        async with get_session() as session:
            stmt = delete(cls).where(cls.user_id == user_id)
            await session.execute(stmt)
