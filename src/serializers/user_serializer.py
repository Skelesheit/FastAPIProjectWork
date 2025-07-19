from datetime import datetime

from pydantic import BaseModel, model_validator

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
        from_attributes = True


# Физическое лицо
class IndividualProfile(BaseModel):
    first_name: str
    last_name: str
    patronymic: str


# Юр. лицо
class LegalEntityProfile(BaseModel):
    org_name: str
    kpp: str
    opf_full: str
    opf_short: str


# ИП
class LegalEntity(BaseModel):
    inn: str
    ogrn: str
    management_name: str
    legal_entity_profile: LegalEntityProfile | None  # если юр. лицо то есть


# полное представление о пользователе (/me)
class UserOut(BaseModel):
    email: str
    created_at: datetime
    user_type: UserType | None
    is_verified: bool
    is_filled: bool
    contact: Contact | None
    individual_profile: IndividualProfile | None
    legal_entity: LegalEntity | None

    class Config:
        from_attributes = True


# заполнить форму пользователя
class UserFillForm(BaseModel):
    contact: Contact
    user_type: UserType
    fill: IndividualProfile | LegalEntity

    @model_validator(mode="before")
    @classmethod
    def resolve_fill(cls, data):
        user_type = data.get("user_type")
        fill_data = data.get("fill")
        if user_type == "ИП":
            data["fill"] = LegalEntity(**fill_data)
        elif user_type == "Физ. лицо":
            data["fill"] = IndividualProfile(**fill_data)
        else:
            raise ValueError("Invalid user_type")

        return data
