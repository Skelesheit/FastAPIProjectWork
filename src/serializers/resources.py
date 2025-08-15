# Обновлённые сериализаторы для всех моделей без связи 1:1
from pydantic import BaseModel

from src.db.enums import MetalType


class ORMBaseModel(BaseModel):
    model_config = {"from_attributes": True}


# --- MaterialCategory ---
class MaterialCategoryBase(BaseModel):
    material_type: MetalType
    name: str


class MaterialCategoryUpdate(BaseModel):
    material_type: MetalType | None = None
    name: str | None = None


class MaterialCategoryCreate(MaterialCategoryBase):
    pass


class MaterialCategoryOut(MaterialCategoryBase, ORMBaseModel):
    id: int
    is_general: bool






# --- OperationType ---
class OperationTypeBase(BaseModel):
    name: str


class OperationTypeCreate(OperationTypeBase):
    pass


class OperationTypeUpdate(BaseModel):
    name: str | None = None


class OperationTypeOut(OperationTypeBase, ORMBaseModel):
    id: int


# --- Method ---
class MethodBase(BaseModel):
    name: str
    operation_type_id: int


class MethodOut(MethodBase, ORMBaseModel):
    id: int


class MethodCreate(MethodBase):
    pass


class MethodUpdate(MethodBase):
    pass


# --- MachineType ---
class MachineTypeBase(BaseModel):
    name: str
    method_id: int


class MachineTypeCreate(MachineTypeBase):
    pass


class MachineTypeUpdate(BaseModel):
    name: str | None = None
    method_id: int | None = None


class MachineTypeOut(MachineTypeBase, ORMBaseModel):
    id: int


# --- Machine ---
class MachineBase(BaseModel):
    name: str
    machine_type_id: int
    count: int
    X: float
    Y: float
    Z: float
    H: float
    D: float


class MachineCreate(MachineBase):
    pass


class MachineUpdate(BaseModel):
    name: str | None = None
    machine_type_id: int | None = None
    count: int | None = None
    X: float | None = None
    Y: float | None = None
    Z: float | None = None
    H: float | None = None
    D: float | None = None


class MachineOut(MachineBase, ORMBaseModel):
    id: int


# --- Tooling ---
class ToolingBase(BaseModel):
    name: str
    mark: str
    gost: str
    machine_id: int
    h_d_foot: float
    B: float
    L: float
    A: float
    h_d: float


class ToolingCreate(ToolingBase):
    pass


class ToolingUpdate(BaseModel):
    name: str | None = None
    mark: str | None = None
    gost: str | None = None
    machine_id: int | None = None
    h_d_foot: float | None = None
    B: float | None = None
    L: float | None = None
    A: float | None = None
    h_d: float | None = None


class ToolingOut(ToolingBase, ORMBaseModel):
    id: int


# --- Tool ---
class ToolBase(BaseModel):
    name: str
    mark: str
    gost: str
    machine_id: int

    K_H_D: float
    alpha_B_d: float
    L: float
    I_max_cut: float
    S: float


class ToolCreate(ToolBase):
    pass


class ToolUpdate(BaseModel):
    name: str | None = None
    mark: str | None = None
    gost: str | None = None
    machine_id: int | None = None

    K_H_D: float | None = None
    alpha_B_d: float | None = None
    L: float | None = None
    I_max_cut: float | None = None
    S: float | None = None


class ToolOut(ToolBase, ORMBaseModel):
    id: int


# Сериализаторы для ассортимента и ГОСТов
from pydantic import BaseModel


class ORMBaseModel(BaseModel):
    model_config = {"from_attributes": True}


# --- GOST ---
class GostBase(BaseModel):
    number: str


class GostCreate(GostBase):
    pass


class GostUpdate(BaseModel):
    number: str | None = None


class GostOut(GostBase, ORMBaseModel):
    id: int
    is_general: bool


# --- AssortmentType ---
class AssortmentTypeBase(BaseModel):
    name: str
    gost_id: int


class AssortmentTypeCreate(AssortmentTypeBase):
    pass


class AssortmentTypeUpdate(BaseModel):
    name: str | None = None
    gost_id: int | None = None


class AssortmentTypeOut(AssortmentTypeBase, ORMBaseModel):
    id: int
    is_general: bool


# --- GostAssortment ---

class GostAssortmentBase(BaseModel):
    gost_id: int
    assortment_type_id: int


class GostAssortmentCreate(GostAssortmentBase):
    pass


class GostAssortmentUpdate(BaseModel):
    gost_id: int | None = None
    assortment_type_id: int | None = None


class GostAssortmentOut(GostAssortmentBase, ORMBaseModel):
    id: int
    gost: GostOut
    assortment_type: AssortmentTypeOut


class GostAssortmentBatchCreate(BaseModel):
    assortment_type_id: int
    gosts: list[int]  # foreign gost ids
    enterprise_id: int


class GostAssortmentBatchOut(BaseModel):
    id: int
    assortment_type_id: int
    gosts: list[int]
    enterprise_id: int


# --- Material ---
class MaterialBase(BaseModel):
    brand: str
    B_D: float
    height: float
    strength: float
    length: float

    dense: float
    hardness: float
    tear_resistance: float
    elongation: float

    comment: str | None = None
    comment_en: str | None = None

    material_category_id: int
    assortment_type_id: int


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    brand: str | None = None
    B_D: float | None = None
    height: float | None = None
    strength: float | None = None
    length: float | None = None

    dense: float | None = None
    hardness: float | None = None
    tear_resistance: float | None = None
    elongation: float | None = None

    comment: str | None = None
    comment_en: str | None = None

    material_category_id: int | None = None
    assortment_type_id: int | None = None


class MaterialOut(MaterialBase, ORMBaseModel):
    id: int
    category: MaterialCategoryOut | None = None
    assortment_type: AssortmentTypeOut | None = None


# --- Assortment ---
class AssortmentBase(BaseModel):
    gost_material_id: int

    B_D: float
    height: float
    strength: float
    length: float

    dense: float
    hardness: float
    tear_resistance: float
    elongation: float


class AssortmentCreate(AssortmentBase):
    pass


class AssortmentUpdate(BaseModel):
    gost_material_id: int | None = None

    B_D: float | None = None
    height: float | None = None
    strength: float | None = None
    length: float | None = None


class AssortmentOut(AssortmentBase, ORMBaseModel):
    id: int
    gost_assortment_model: GostAssortmentOut
