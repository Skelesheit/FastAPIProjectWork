from sqlalchemy import String, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enterprise_base import EnterpriseBase, EnterpriseGeneralBase
from src.db.enums import MetalType, metal_type_enum


class MaterialCategory(EnterpriseGeneralBase):
    __tablename__ = 'material_category'

    __table_args__ = (
        UniqueConstraint(
            'enterprise_id',
            'name',
            name='uq_materialcategory_enterprise_name'),
    )

    material_type: Mapped[MetalType] = mapped_column(metal_type_enum)

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

    assortment_types: Mapped[list['AssortmentType']] = relationship(
        'AssortmentType',
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
    gost_id: Mapped[int] = mapped_column(
        ForeignKey('gost.id'),
        nullable=False,
    )

    gost: Mapped[Gost] = relationship(
        'Gost',
        back_populates='assortment_types',
    )

    materials: Mapped[list['Material']] = relationship(
        'Material',
        back_populates='assortment_type',
    )

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='assortment_types',
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
    dense: Mapped[float] = mapped_column(Float())
    hardness: Mapped[float] = mapped_column(Float())
    tear_resistance: Mapped[float] = mapped_column(Float())
    elongation: Mapped[float] = mapped_column(Float())

    DB: Mapped[float] = mapped_column(Float())
    height: Mapped[float] = mapped_column(Float())
    strength: Mapped[float] = mapped_column(Float())
    length: Mapped[float] = mapped_column(Float())

    comment: Mapped[str] = mapped_column(String())
    comment_en: Mapped[str] = mapped_column(String())

    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            'material_category.id'
        ),
        nullable=False,
    )
    assortment_type_id: Mapped[int] = mapped_column(
        ForeignKey(
            'assortment_type.id'
        ),
        nullable=False,
    )

    category: Mapped[MaterialCategory] = relationship(
        'MaterialCategory',
        back_populates='materials',
    )
    assortment_type: Mapped[AssortmentType] = relationship(
        'AssortmentType',
        back_populates='materials',
    )

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='materials',
    )
