from pydantic import BaseModel, model_validator

from src.db.enums import EnterpriseType, MemberRole, MemberStatus


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

    class Config:
        from_attributes = True


# Юр. лицо
class LegalEntityProfile(BaseModel):
    org_name: str
    kpp: str
    opf_full: str
    opf_short: str

    class Config:
        from_attributes = True


# ИП
class LegalEntity(BaseModel):
    inn: str
    ogrn: str
    management_name: str
    legal_entity_profile: LegalEntityProfile | None  # если юр. лицо то есть

    class Config:
        from_attributes = True


# заполнить форму пользователя
class EnterpriseFillForm(BaseModel):
    name: str
    contact: Contact
    enterprise_type: EnterpriseType
    fill: IndividualProfile | LegalEntity

    @model_validator(mode='before')
    @classmethod
    def resolve_fill(cls, data):
        enterprise_type = data.get('enterprise_type')
        fill_data = data.get('fill')
        if isinstance(enterprise_type, str):
            enterprise_type = EnterpriseType(enterprise_type)
        match enterprise_type:
            case EnterpriseType.LegalEntity:
                data['fill'] = LegalEntity(**fill_data)
            case EnterpriseType.LegalEntityProfile:
                data['fill'] = LegalEntity(**fill_data)
            case EnterpriseType.Individual:
                data['fill'] = IndividualProfile(**fill_data)
            case _:
                raise ValueError('Invalid enterprise_type')
        return data


class EnterpriseMemberOut(BaseModel):
    id: int
    email: str
    role: MemberRole
    status: MemberStatus

    class Config:
        from_attributes = True


class EnterpriseOut(BaseModel):
    id: int
    name: str
    enterprise_type: str
    contact: Contact | None
    individual_profile: IndividualProfile | None
    legal_entity: LegalEntity | None
    members: list[EnterpriseMemberOut]

    class Config:
        from_attributes = True
