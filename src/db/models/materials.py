from sqlalchemy import String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enterprise_base import EnterpriseBase, EnterpriseGeneralBase
from src.db.enums import MetalType


class MaterialCategory(EnterpriseGeneralBase):
    __tablename__ = 'material_category'

    __table_args__ = (
        UniqueConstraint(
            'enterprise_id',
            'name',
            name='uq_materialcategory_enterprise_name'),
    )

    material_type: Mapped[MetalType] = mapped_column(
        PG_ENUM(
            MetalType,
            name='metal_type_enum',
            create_type=False,
            reuse_existing=True,
        )
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    @classmethod
    def field_name(cls) -> str:
        return 'name'

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='material_categories',
    )

    materials: Mapped[list['Material']] = relationship(
        'Material',
        back_populates='category',
    )


class Material(EnterpriseBase):
    __tablename__ = 'material'

    __table_args__ = (
        UniqueConstraint(
            'enterprise_id',
            'brand',
            name='uq_materialcategory_brand_name'
        ),
    )

    brand: Mapped[str] = mapped_column(String(200), nullable=False)
    dense: Mapped[float] = mapped_column(Float)
    hardness: Mapped[float] = mapped_column(Float)
    tear_resistance: Mapped[float] = mapped_column(Float)
    elongation: Mapped[float] = mapped_column(Float)

    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            'material_category.id'
        ),
        nullable=False,
    )

    category: Mapped[MaterialCategory] = relationship(
        'MaterialCategory',
        back_populates='materials',
    )

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='materials',
    )


class Gost(EnterpriseGeneralBase):
    __tablename__ = 'gost'

    __table_args__ = (
        UniqueConstraint(
            'enterprise_id',
            'number',
            name='uq_enterprise_gost_number'),
    )

    @classmethod
    def field_name(cls) -> str:
        return 'number'

    number: Mapped[str] = mapped_column(String(200), nullable=False)

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='gosts',
    )
    gost_assortments: Mapped[list['GostAssortment']] = relationship(
        'GostAssortment',
        back_populates='gost',
    )


class AssortmentType(EnterpriseGeneralBase):
    __tablename__ = 'assortment_type'
    __table_args__ = (
        UniqueConstraint(
            'enterprise_id',
            'name',
            name='uq_enterprise_assortment_type_name'
        ),
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='assortment_types',
    )

    gost_assortments: Mapped[list['GostAssortment']] = relationship(
        'GostAssortment',
        back_populates='assortment_type',
    )


class GostAssortment(EnterpriseGeneralBase):
    __tablename__ = 'gost_assortment'
    __table_args__ = (
        UniqueConstraint('gost_id', 'assortment_type_id'),)

    assortment_type_id: Mapped[int] = mapped_column(
        ForeignKey(
            'assortment_type.id'
        ),
        nullable=False,
    )
    gost_id: Mapped[int] = mapped_column(
        ForeignKey(
            'gost.id'
        ),
        nullable=False,
    )

    gost: Mapped['Gost'] = relationship(
        'Gost',
        uselist=False,
        back_populates='gost_assortments',
    )

    assortment_type: Mapped['AssortmentType'] = relationship(
        'AssortmentType',
        uselist=False,
        back_populates='gost_assortments',
    )

    assortments: Mapped[list['Assortment']] = relationship(
        'Assortment',
        back_populates='gost_assortment_model',
    )

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='gost_assortments',
    )

    @classmethod
    def field_name(cls) -> str:
        return 'id'


class Assortment(EnterpriseBase):
    __tablename__ = 'assortment'

    gost_material_id: Mapped[int] = mapped_column(
        ForeignKey(
            'gost_assortment.id',
            ondelete='CASCADE'
        ),
        nullable=False,
    )
    B_D: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)
    strength: Mapped[float] = mapped_column(Float)
    length: Mapped[float] = mapped_column(Float)

    gost_assortment_model: Mapped['GostAssortment'] = relationship(
        'GostAssortment',
        back_populates='assortments',
        uselist=False
    )

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='assortments',
    )
