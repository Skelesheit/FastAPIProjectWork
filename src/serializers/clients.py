from pydantic import BaseModel


class Management(BaseModel):
    name: str | None = None

class OrganizationName(BaseModel):
    full_with_opf: str | None = None

class OrganizationForm(BaseModel):
    full: str | None = None
    short: str | None = None

class AddressData(BaseModel):
    city: str | None = None

class Address(BaseModel):
    value: str | None = None
    data: AddressData | None = None

# Основная модель для ответа клиенту
class DadataOrganization(BaseModel):
    ogrn: str | None = None
    inn: str | None = None
    kpp: str | None = None
    management: Management | None = None
    name: OrganizationName | None = None
    opf: OrganizationForm | None = None
    address: Address | None = None

    class Config:
        # Для красивого отображения в документации
        json_schema_extra = {
            "example": {
                "ogrn": "1027700132195",
                "inn": "7707083893",
                "kpp": "770701001",
                "management": {
                    "name": "Иванов Иван Иванович"
                },
                "name": {
                    "full_with_opf": "ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО \"СБЕРБАНК РОССИИ\""
                },
                "opf": {
                    "full": "Публичное акционерное общество",
                    "short": "ПАО"
                },
                "address": {
                    "value": "г Москва, ул Вавилова, д 19",
                    "data": {
                        "city": "Москва"
                    }
                }
            }
        }