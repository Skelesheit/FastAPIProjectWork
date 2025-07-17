from fastapi import APIRouter
from starlette.responses import RedirectResponse

from config import settings
from src.services.client import ClientService

client_router = APIRouter()


@client_router.get("/mail/<string:inn>")
async def mail(token: str):
    await ClientService.verify_mail(token)
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/email-confirmed")


@client_router.post("/dadata/<string:inn>")
async def get_dadata_suggest(inn: str):
    data = await ClientService.suggest_company_by_inn(inn)
    return data
