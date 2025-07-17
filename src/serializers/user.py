from datetime import datetime

from pydantic import BaseModel

from src.db.enums import UserType


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(UserLogin):
    captcha: str


class Contact(BaseModel):
    phone: str
    city: str
    address: str

    class Config:
        orm_mode = True


# Физическое лицо
class IndividualProfile(BaseModel):
    first_name: str
    last_name: str
    patronymic: str


# ИП
class LegalEntity(BaseModel):
    inn: str
    ogrn: str
    management_name: str
    profile: IndividualProfile | None  # если юр. лицо то есть


# Юр. лицо
class LegalEntityProfile(BaseModel):
    org_name: str
    kpp: str
    opf_full: str
    opf_short: str


# полное представление о пользователе (/me)
class UserOut(BaseModel):
    email: str
    created_at: datetime
    user_type: UserType
    is_verified: bool
    is_filled: bool
    is_admin: bool
    contact: Contact
    extra: IndividualProfile | LegalEntity | None

    class Config:
        orm_mode = True


# заполнить форму пользователя
class UserFillForm(BaseModel):
    id: int | None
    contact: Contact
    type: UserType
    fill: IndividualProfile | LegalEntity
