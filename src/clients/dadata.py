import httpx

from config import settings
from src.serializers.clients import (
    DadataOrganization,
    OrganizationForm,
    Address,
    AddressData,
    OrganizationName,
    Management
)


def parse_dadata_organization(dadata_response: dict) -> DadataOrganization:
    """
    Преобразует ответ от DaData API в нашу Pydantic модель
    """
    return DadataOrganization(
        ogrn=dadata_response.get("ogrn"),
        inn=dadata_response.get("inn"),
        kpp=dadata_response.get("kpp"),
        management=Management(
            name=dadata_response.get("management", {}).get("name")
        ) if dadata_response.get("management") else None,
        name=OrganizationName(
            full_with_opf=dadata_response.get("name", {}).get("full_with_opf")
        ) if dadata_response.get("name") else None,
        opf=OrganizationForm(
            full=dadata_response.get("opf", {}).get("full"),
            short=dadata_response.get("opf", {}).get("short")
        ) if dadata_response.get("opf") else None,
        address=Address(
            value=dadata_response.get("address", {}).get("value"),
            data=AddressData(
                city=dadata_response.get("address", {}).get("data", {}).get("city")
            ) if dadata_response.get("address", {}).get("data") else None
        ) if dadata_response.get("address") else None
    )

async def suggest_company_by_inn(query: str) -> DadataOrganization:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {settings.DADATA_TOKEN}"
    }
    body = {"query": query}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.DADATA_API_URL,
            headers=headers,
            json=body
        )
    suggestions = response.json().get("suggestions", [])
    dadata_data = suggestions[0]["data"]
    return parse_dadata_organization(dadata_data)
