from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.db.enums import OperationType, MetalType


class Machine(Base):
    __tablename__ = 'machine'

    name: Mapped[str] = mapped_column(String(200), primary_key=True)


class Metal(Base):
    __tablename__ = 'metal'

    metal_type: Mapped[MetalType] = mapped_column(
        PG_ENUM(MetalType, name="metal_type_enum", create_type=True),
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)


class Operation(Base):
    __tablename__ = 'operation'

    operation_type: Mapped[OperationType] = mapped_column(
        PG_ENUM(OperationType, name="operation_type_enum", create_type=True),
        nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)


class Material(Base):
    __tablename__ = 'material'

    name: Mapped[str] = mapped_column(String(200), nullable=False)


class GOST(Base):
    __tablename__ = 'gost'

    number: Mapped[str] = mapped_column(String(100), nullable=False)


class GOSTMaterial(Base):
    __tablename__ = 'gost_material'

    material_id: Mapped[int] = mapped_column(ForeignKey('material.id'), nullable=False)
    gost_id: Mapped[int] = mapped_column(ForeignKey('gost.id'), nullable=False)
