from enum import Enum

from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM


class OperationType(str, Enum):
    CUTTING = "Обработка резанием"
    PRESSING = "Обработка давлением"


class MetalType(str, Enum):
    NONFERROUS = "Металлы цветные"
    FERROUS = "Металлы черные"
    NONMETALLIC = "Неметаллические материалы"


class EnterpriseType(str, Enum):
    Individual = 'Физ. лицо'
    LegalEntity = 'ИП'
    LegalEntityProfile = 'Юр. лицо'


class MemberRole(str, Enum):
    OWNER = "owner"  # Владелец компании
    ADMIN = "admin"  # Администратор
    MANAGER = "manager"  # Руководитель отдела / проекта
    EMPLOYEE = "employee"  # Обычный сотрудник
    INTERN = "intern"  # Стажёр
    OTHER = "other"


class MemberStatus(str, Enum):
    INVITED = "invited"  # Приглашён, но не принял приглашение
    ACTIVE = "active"  # Активный член компании
    SUSPENDED = "suspended"  # Временно отстранён
    LEFT = "left"  # Вышел из компании
    REMOVED = "removed"  # Был удалён админом/владельцем


metal_type_enum = PG_ENUM(
    MetalType, name="metal_type_enum",
    create_type=False, reuse_existing=True
)

enterprise_type_enum = PG_ENUM(
    EnterpriseType, name="enterprise_type_enum",
    create_type=False, reuse_existing=True
)

member_role_enum = PG_ENUM(
    MemberRole, name="member_role_enum",
    create_type=False, reuse_existing=True
)

member_status_enum = PG_ENUM(
    MemberStatus, name="member_status_enum",
    create_type=False, reuse_existing=True
)
