import secrets
from datetime import datetime, timedelta
from typing import TypeVar, Type, Any

from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Integer, String, func
from sqlalchemy import update, select, delete
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

from config import settings
from src.auth.hash import validate, hash_password
from src.db import get_session

T = TypeVar('T', bound='BaseModel')


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

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

    async def update_by_id(self, id_: int, **kwargs) -> None:
        async with get_session() as session:
            stmt = update(type(self)).where(type(self).id == id_).values(**kwargs)
            await session.execute(stmt)


class User(Base):
    __tablename__ = 'user'
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_type = Column(ENUM('ИП', 'Юр. лицо', 'Физ. лицо', name='user_type_enum'), )
    is_verified = Column(Boolean, nullable=False, default=False)
    is_filled = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    token = relationship('RefreshToken', back_populates='user', uselist=False, cascade='all, delete-orphan')
    contact = relationship('Contact', back_populates='user', uselist=False, cascade='all, delete-orphan')
    individual_profile = relationship('IndividualProfile', back_populates='user', uselist=False,
                                      cascade='all, delete-orphan')
    legal_entity = relationship('LegalEntity', back_populates='user', uselist=False, cascade='all, delete-orphan')

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
    async def get_by_id(cls, user_id: int) -> 'User | None':
        async with get_session() as session:
            stmt = select(cls).where(cls.id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

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
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    token = Column(String(), nullable=False)
    expires_at = Column(DateTime(), nullable=False)

    user = relationship('User', back_populates='token', uselist=False)

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

    @classmethod
    async def delete(cls) -> None:
        async with get_session() as session:
            await session.execute(delete(cls))


# контактная информация
class Contact(Base):
    __tablename__ = 'contact_info'
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    phone = Column(String(15), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(300), nullable=False)

    user = relationship('User', back_populates='contact', uselist=False)


# физическое лицо
class IndividualProfile(Base):
    __tablename__ = 'profile_individual'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    patronymic = Column(String(100), nullable=False)

    user = relationship('User', back_populates='individual_profile', uselist=False)


# юридическое лицо (база)
class LegalEntity(Base):
    __tablename__ = 'legal_entity'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    inn = Column(String(12), nullable=False)
    ogrn = Column(String(13), nullable=False)
    management_name = Column(String(300))

    user = relationship('User', back_populates='legal_entity', uselist=False)
    legal_entity_profile = relationship('LegalEntityProfile', back_populates='legal_entity', uselist=False,
                                        cascade='all, delete-orphan')


# юридическое лицо - расширение (не ИП)
class LegalEntityProfile(Base):
    __tablename__ = 'profile_legal_entity'
    legal_id = Column(Integer, ForeignKey('legal_entity.id'), nullable=False)
    org_name = Column(String(), nullable=False)
    kpp = Column(String(9), nullable=False)
    opf_full = Column(String(), nullable=False)
    opf_short = Column(String(30), nullable=False)

    legal_entity = relationship('LegalEntity', back_populates='legal_entity_profile', uselist=False)
