import secrets
from datetime import datetime, timedelta
from typing import Literal

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, String, func
from sqlalchemy import update, select, delete
from sqlalchemy.orm import relationship, Mapped, mapped_column

from config import settings
from src.auth.hash import validate, hash_password
from src.db import get_session
from src.db.base import Base
from src.db.enums import user_type_postgres

UserTypeLiteral = Literal['ИП', 'Юр. лицо', 'Физ. лицо']


class User(Base):
    __tablename__ = 'user'

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    user_type: Mapped[UserTypeLiteral] = mapped_column(user_type_postgres, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_filled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    token: Mapped['RefreshToken'] = relationship(
        'RefreshToken', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    contact: Mapped['Contact'] = relationship(
        'Contact', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    individual_profile: Mapped['IndividualProfile'] = relationship(
        'IndividualProfile', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )
    legal_entity: Mapped['LegalEntity'] = relationship(
        'LegalEntity', back_populates='user', uselist=False, cascade='all, delete-orphan'
    )

    @classmethod
    async def create(cls, email, password) -> 'User':
        password_hash = hash_password(password)
        async with get_session() as session:
            user = User(email=email, password=password_hash)
            session.add(user)
            await session.flush()
            await session.refresh(user)
        return user

    @classmethod
    async def verify_email(cls, user_id: int) -> bool:
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
        async with get_session() as session:
            stmt = select(cls).where(cls.email == email)
            result = await session.execute(stmt)
            return result.rowcount > 0

    @classmethod
    async def get_by_email(cls, email: str) -> 'User | None':
        async with get_session() as session:
            stmt = select(cls).where(cls.email == email)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    def check_password(self, password: str) -> bool:
        return validate(password, self.password)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


class RefreshToken(Base):
    __tablename__ = 'token'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    token: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='token', uselist=False)

    @property
    def expired(self) -> bool:
        return self.expires_at < datetime.now()

    @classmethod
    async def get_by_token(cls, token: str) -> 'RefreshToken':
        async with get_session() as session:
            stmt = select(cls).where(cls.token == token)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def delete_by_token(cls, token: str) -> None:
        async with get_session() as session:
            stmt = delete(cls).where(cls.token == token)
            await session.execute(stmt)

    @classmethod
    async def create(cls, user_id: int) -> 'RefreshToken':
        """
        Удаляет старый токен и создаёт новый
        :param user_id: id Пользователя
        :return:
        """
        await cls.delete_by_user_id(user_id)
        token = secrets.token_urlsafe(64)
        expires = datetime.now() + timedelta(days=settings.expire_refresh_token_time)
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


# контактная информация
class Contact(Base):
    __tablename__ = 'contact_info'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(300), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='contact', uselist=False)


# физическое лицо
class IndividualProfile(Base):
    __tablename__ = 'profile_individual'

    user_id: Mapped[int] = Column(Integer, ForeignKey('user.id'), nullable=False)
    first_name: Mapped[str] = Column(String(100), nullable=False)
    last_name: Mapped[str] = Column(String(100), nullable=False)
    patronymic: Mapped[str] = Column(String(100), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='individual_profile', uselist=False)


class LegalEntity(Base):
    __tablename__ = 'legal_entity'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    inn: Mapped[str] = mapped_column(String(12), nullable=False)
    ogrn: Mapped[str] = mapped_column(String(13), nullable=False)
    management_name: Mapped[str | None] = mapped_column(String(300), nullable=True)

    user: Mapped['User'] = relationship('User', back_populates='legal_entity', uselist=False)

    legal_entity_profile: Mapped['LegalEntityProfile'] = relationship(
        'LegalEntityProfile',
        back_populates='legal_entity',
        uselist=False,
        cascade='all, delete-orphan'
    )


# юридическое лицо - расширение (не ИП)
class LegalEntityProfile(Base):
    __tablename__ = 'profile_legal_entity'

    legal_id: Mapped[int] = mapped_column(ForeignKey('legal_entity.id'), nullable=False)
    org_name: Mapped[str] = mapped_column(String, nullable=False)
    kpp: Mapped[str] = mapped_column(String(9), nullable=False)
    opf_full: Mapped[str] = mapped_column(String, nullable=False)
    opf_short: Mapped[str] = mapped_column(String(30), nullable=False)

    legal_entity: Mapped['LegalEntity'] = relationship(
        'LegalEntity',
        back_populates='legal_entity_profile',
        uselist=False
    )