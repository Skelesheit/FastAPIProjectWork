from fastapi import APIRouter
from starlette.responses import RedirectResponse, JSONResponse

from config import settings
from src.services.client_service import ClientService, ServiceException

client_router = APIRouter()


@client_router.get("/mail/{token}")
async def mail(token: str):
    print(f"Token is: {token}")
    await ClientService.verify_mail(token)
    return RedirectResponse(url=f"{settings.FRONTEND_URL}/email-confirmed")


@client_router.post("/dadata/{inn}")
async def get_dadata_suggest(inn: str):
    try:
        return await ClientService.suggest_company_by_inn(inn)
    except ServiceException as e:
        return JSONResponse(content=e.json_message, status_code=403)
