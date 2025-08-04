from __future__ import annotations

from datetime import datetime

from sqlalchemy import ForeignKey, String, func, DateTime, UniqueConstraint, exists
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, relationship, selectinload, joinedload

from src.db import get_session
from src.db.base import Base
from src.db.enums import MemberRole, MemberStatus, EnterpriseType


class Enterprise(Base):
    __tablename__ = 'enterprise'

    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    enterprise_type: Mapped[EnterpriseType] = mapped_column(
        PG_ENUM(
            EnterpriseType,
            name='enterprise_type_enum',
            create_type=False),
    )

    members: Mapped[list['EnterpriseMember']] = relationship(
        'EnterpriseMember',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )

    owner: Mapped['User'] = relationship('User', lazy="joined")

    contact: Mapped['Contact'] = relationship(
        'Contact',
        back_populates='enterprise',
        uselist=False,
        cascade='all, delete-orphan'
    )
    individual_profile: Mapped['IndividualProfile'] = relationship(
        'IndividualProfile',
        back_populates='enterprise',
        uselist=False,
        cascade='all, delete-orphan'
    )
    legal_entity: Mapped['LegalEntity'] = relationship(
        'LegalEntity',
        back_populates='enterprise',
        uselist=False,
        cascade='all, delete-orphan'
    )

    material_categories: Mapped[list['MaterialCategory']] = relationship(
        'MaterialCategory',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    materials: Mapped[list['Material']] = relationship(
        'Material',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    gosts: Mapped[list['Gost']] = relationship(
        'Gost',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    assortment_types: Mapped[list['AssortmentType']] = relationship(
        'AssortmentType',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    gost_assortments: Mapped[list['GostAssortment']] = relationship(
        'GostAssortment',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    assortments: Mapped[list['Assortment']] = relationship(
        'Assortment',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )

    operation_types: Mapped[list['OperationType']] = relationship(
        'OperationType',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    methods: Mapped[list['Method']] = relationship(
        'Method',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    machine_types: Mapped[list['MachineType']] = relationship(
        'MachineType',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    machines: Mapped[list['Machine']] = relationship(
        'Machine',
        back_populates='enterprise',
        cascade='all, delete-orphan'
    )
    material_categories: Mapped['MaterialCategory'] = relationship(
        'MaterialCategory',
        back_populates='enterprise',
    )
    toolings: Mapped[list['Tooling']] = relationship(
        'Tooling',
        back_populates='enterprise'
    )
    tools: Mapped[list['Tool']] = relationship(
        'Tool',
        back_populates='enterprise'
    )

    async def delete_member(self, member_id: int) -> bool:
        from src.db.models import User
        async with get_session() as session:
            stmt = (
                select(EnterpriseMember)
                .where(EnterpriseMember.id == member_id,
                       EnterpriseMember.enterprise_id == self.id)
            )
            result = await session.execute(stmt)
            member = result.scalar_one_or_none()
            if member is None:
                return False
            stmt = select(User).where(User.id == member.user_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                return False
            user.is_member = False
            session.add(user)
            await session.delete(member)
        return True

    @classmethod
    async def get_enterprise_by_owner(cls, user_id: int) -> Enterprise | None:
        async with get_session() as session:
            stmt = select(cls).where(cls.owner_id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_by_inn(cls, inn: str) -> Enterprise | None:
        async with get_session() as session:
            stmt = (
                select(cls)
                .options(joinedload(cls.legal_entity))
                .where(cls.legal_entity.has(inn=inn)))
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @staticmethod
    async def get_enterprise_inn_by_owner(owner_id: int) -> str:
        async with get_session() as session:
            stmt = (
                select(LegalEntity.inn)
                .join(Enterprise)
                .where(Enterprise.owner_id == owner_id)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all_data(cls, _id: int) -> Enterprise | None:
        async with get_session() as session:
            stmt = (
                select(cls)
                .where(cls.id == _id)
                .options(
                    selectinload(cls.members).joinedload(EnterpriseMember.user),
                    selectinload(cls.owner),
                    selectinload(cls.contact),
                    selectinload(cls.individual_profile),
                    selectinload(cls.legal_entity),
                    selectinload(cls.legal_entity).selectinload(LegalEntity.legal_entity_profile)
                )
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    def __repr__(self):
        return f"<Enterprise id={self.id} name={self.name}>"


class EnterpriseMember(Base):
    __tablename__ = 'enterprise_member'
    __table_args__ = (
        UniqueConstraint('enterprise_id', 'user_id'),
    )

    enterprise_id: Mapped[int] = mapped_column(ForeignKey('enterprise.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True)
    role: Mapped[MemberRole] = mapped_column(
        PG_ENUM(
            MemberRole,
            name='role_enum',
            create_type=True),
        default=MemberRole.EMPLOYEE
    )
    status: Mapped[MemberStatus] = mapped_column(
        PG_ENUM(
            MemberStatus,
            name='status_enum',
            create_type=True),
        default=MemberStatus.INVITED
    )
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='members'
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='enterprise_member',
        uselist=False,
        lazy="joined"
    )

    @staticmethod
    async def has_email_with_session(session: AsyncSession, email: str) -> bool:
        from src.db.models.users import User
        stmt = select(
            exists(
                select(1)
                .select_from(EnterpriseMember)
                .join(User, EnterpriseMember.user_id == User.id)
                .where(User.email == email)
            )
        )
        result = await session.execute(stmt)
        return result.scalar()

    @classmethod
    async def get_enterprise_id_by_user_id(cls, user_id: int) -> int | None:
        async with get_session() as session:
            stmt = (
                select(EnterpriseMember.enterprise_id)
                .where(EnterpriseMember.user_id == user_id)
            )
            result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @property
    def email(self) -> str:
        return self.user.email

    def __repr__(self):
        return f"<EnterpriseMember user_id={self.user_id} role={self.role}>"


# контактная информация
class Contact(Base):
    __tablename__ = 'contact_info'

    enterprise_id: Mapped[int] = mapped_column(ForeignKey('enterprise.id'), nullable=False)
    phone: Mapped[str] = mapped_column(String(15), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(300), nullable=False)

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='contact',
        uselist=False
    )


# физическое лицо
class IndividualProfile(Base):
    __tablename__ = 'profile_individual'

    enterprise_id: Mapped[int] = mapped_column(ForeignKey('enterprise.id'), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=False)

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='individual_profile',
        uselist=False
    )


class LegalEntity(Base):
    __tablename__ = 'legal_entity'

    enterprise_id: Mapped[int] = mapped_column(ForeignKey('enterprise.id'), nullable=False)
    inn: Mapped[str] = mapped_column(String(12), nullable=False)
    ogrn: Mapped[str] = mapped_column(String(13), nullable=False)
    management_name: Mapped[str | None] = mapped_column(String(300), nullable=True)

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='legal_entity',
        uselist=False
    )
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
    org_name: Mapped[str] = mapped_column(String(200), nullable=False)
    kpp: Mapped[str] = mapped_column(String(9), nullable=False)
    opf_full: Mapped[str] = mapped_column(String, nullable=False)
    opf_short: Mapped[str] = mapped_column(String(30), nullable=False)

    legal_entity: Mapped['LegalEntity'] = relationship(
        'LegalEntity',
        back_populates='legal_entity_profile',
        uselist=False
    )
