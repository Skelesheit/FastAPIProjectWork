from typing import Annotated

from fastapi import APIRouter, Path
from starlette.responses import RedirectResponse, JSONResponse

from config import settings
from src.serializers.clients import DadataOrganization
from src.services.client_service import ClientService
from src.services.enterprise_service import EnterpriseService

client_router = APIRouter()

@client_router.get("/mail/{token}")
async def mail(token: str):
    await ClientService.verify_mail(token)
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/email-confirmed")


@client_router.get("/mail/join-to-enterprise/{token}")
async def mail_join(token: str):
    # TODO: поправить чтобы токены работали - генерились и валидировались
    await EnterpriseService.join_by_email(token)
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/success-to-join")


@client_router.get("/dadata/{inn}")
async def get_dadata_suggest(
        inn: Annotated[str, Path(
            regex=r"^\d{10}$|^\d{12}$",  # 10 или 12 цифр
            description="ИНН организации (10 цифр) или ИП (12 цифр)",
            example="1234567890"
        )]
)-> DadataOrganization:
    return await ClientService.suggest_company_by_inn(inn)
