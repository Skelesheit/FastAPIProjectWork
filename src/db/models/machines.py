from sqlalchemy import String, ForeignKey, Float, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.enterprise_base import EnterpriseBase, EnterpriseGeneralBase


# тип операции
class OperationType(EnterpriseGeneralBase):
    __tablename__ = 'operation_type'

    __table_args__ = tuple(
        UniqueConstraint(
            "enterprise_id",
            "name",
            name="uq_operationtype_enterprise_name"
        ),
    )

    @classmethod
    def field_name(cls) -> str:
        return 'name'

    name: Mapped[str] = mapped_column(String(100))

    methods: Mapped[list['Method']] = relationship(
        'Method',
        back_populates='operation_type',
        cascade='all, delete-orphan'  # если Method привязан только к этому типу
    )

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='operation_types'  # ← если есть в Enterprise
    )


# метод обработки
class Method(EnterpriseGeneralBase):
    __tablename__ = 'method'

    __table_args__ = tuple(
        UniqueConstraint(
            'enterprise_id',
            'name',
            name="uq_method_enterprise_name"
        ),
    )

    name: Mapped[str] = mapped_column(String(100))
    operation_type_id: Mapped[int] = mapped_column(
        ForeignKey(
            'operation_type.id'
        ),
        nullable=False
    )

    @classmethod
    def field_name(cls) -> str:
        return 'name'

    operation_type: Mapped['OperationType'] = relationship(
        'OperationType',
        back_populates='methods'
    )

    # Прямая связь к MachineType
    machine_types: Mapped[list['MachineType']] = relationship(
        'MachineType',
        back_populates='method',
        cascade='all, delete-orphan'
    )

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='methods'
    )


# тип станка
class MachineType(EnterpriseGeneralBase):
    __tablename__ = 'machine_type'

    __table_args__ = tuple(
        UniqueConstraint(
            'enterprise_id',
            'name',
            name='uq_machinetype_enterprise_name'
        ),
    )

    name: Mapped[str] = mapped_column(String(100))
    method_id: Mapped[int] = mapped_column(
        ForeignKey(
            'method.id'
        ),
        nullable=False
    )

    @classmethod
    def field_name(cls) -> str:
        return 'name'

    method: Mapped['Method'] = relationship(
        'Method',
        back_populates='machine_types'
    )

    # Прямая связь к Machine
    machines: Mapped[list['Machine']] = relationship(
        'Machine',
        back_populates='machine_type',
        cascade='all, delete-orphan'
    )

    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='machine_types'
    )


# станок
class Machine(EnterpriseBase):
    __tablename__ = 'machine'

    __table_args__ = tuple(
        UniqueConstraint(
            'enterprise_id',
            'name',
            name='uq_machine_enterprise_name'
        ),
    )

    X: Mapped[float] = mapped_column(Float)
    Y: Mapped[float] = mapped_column(Float)
    Z: Mapped[float] = mapped_column(Float)
    H: Mapped[float] = mapped_column(Float)
    D: Mapped[float] = mapped_column(Float)
    name: Mapped[str] = mapped_column(String(100))
    machine_type_id: Mapped[int] = mapped_column(
        ForeignKey(
            'machine_type.id'
        ),
        nullable=False
    )
    count: Mapped[int] = mapped_column(Integer, default=1)

    @classmethod
    def field_name(cls) -> str:
        return 'name'

    machine_type: Mapped['MachineType'] = relationship(
        'MachineType',
        back_populates='machines'
    )
    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='machines'
    )
    toolings: Mapped[list['Tooling']] = relationship(
        'Tooling',
        back_populates='machine',
        cascade='all, delete-orphan'
    )
    tools: Mapped[list['Tool']] = relationship(
        'Tool',
        back_populates='machine',
        cascade='all, delete-orphan'
    )


# оснастка
class Tooling(EnterpriseBase):
    __tablename__ = 'tooling'

    __table_args__ = tuple(
        UniqueConstraint(
            'enterprise_id',
            'name',
            name='uq_tooling_enterprise_name'
        ),
    )

    h_d_foot: Mapped[float] = mapped_column(Float)
    B: Mapped[float] = mapped_column(Float)
    L: Mapped[float] = mapped_column(Float)
    A: Mapped[float] = mapped_column(Float)
    h_d: Mapped[float] = mapped_column(Float)

    name: Mapped[str] = mapped_column(String(100))
    mark: Mapped[str] = mapped_column(String(100))
    gost: Mapped[str] = mapped_column(String(100), nullable=False)

    @classmethod
    def field_name(cls) -> str:
        return 'name'

    machine_id: Mapped[int] = mapped_column(
        ForeignKey('machine.id'),
        nullable=False
    )

    # Связь с машиной
    machine: Mapped['Machine'] = relationship(
        'Machine',
        back_populates='toolings',  # машина имеет список оснастки
    )

    # Привязка к предприятию
    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='toolings'
    )


# инструмент
class Tool(EnterpriseBase):
    __tablename__ = 'tool'

    __table_args__ = tuple(
        UniqueConstraint(
            'enterprise_id',
            'name',
            name='uq_tool_enterprise_name'
        ),
    )

    K_H_D: Mapped[float] = mapped_column(Float)
    alpha_B_d: Mapped[float] = mapped_column(Float)
    L: Mapped[float] = mapped_column(Float)
    I_max_cut: Mapped[float] = mapped_column(Float)
    S: Mapped[float] = mapped_column(Float)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    mark: Mapped[str] = mapped_column(String(100), nullable=False)
    gost: Mapped[str] = mapped_column(String(100), nullable=False)

    machine_id: Mapped[int] = mapped_column(
        ForeignKey(
            'machine.id'
        ),
        nullable=False
    )

    @classmethod
    def field_name(cls) -> str:
        return 'name'

    # Связь с машиной
    machine: Mapped['Machine'] = relationship(
        'Machine',
        back_populates='tools'  # машина имеет список инструментов
    )

    # Привязка к предприятию
    enterprise: Mapped['Enterprise'] = relationship(
        'Enterprise',
        back_populates='tools'
    )
