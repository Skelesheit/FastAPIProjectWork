from fastapi import APIRouter, Depends, HTTPException

from src.auth.dep import get_enterprise_by_owner, get_current_user_id, get_enterprise_inn_by_owner
from src.db.models import EnterpriseType, Enterprise
from src.serializers.token import InviteTokenOut, JoinTokenIn
from src.serializers.enterprise import EnterpriseFillForm
from src.services import ServiceException
from src.services.enterprise_service import EnterpriseService

enterprise_router = APIRouter()

@enterprise_router.post("/create")
async def create_enterprise(dto: EnterpriseFillForm, user_id: int = Depends(get_current_user_id)):
    return await EnterpriseService.create(dto, user_id)

@enterprise_router.get("/generate-tokens/{count}", response_model=InviteTokenOut)
async def generate_tokens(count: int, inn: str = Depends(get_enterprise_inn_by_owner)):
    tokens = await EnterpriseService.create_invite_token(inn, count)
    return InviteTokenOut(tokens=tokens)


@enterprise_router.post("/join-to-enterprise")
async def join_to_company(dto: JoinTokenIn, user_id: int = Depends(get_current_user_id)):
    is_invited = await EnterpriseService.join_by_token(dto, user_id)
    if not is_invited:
        raise HTTPException(status_code=404, detail="Invalid token")
    return {"message": "Пользователь успешно присоединён"}

@enterprise_router.get("/revoke/{member_id}")
async def revoke(member_id: int, enterprise: Enterprise = Depends(get_enterprise_by_owner)):
    if await EnterpriseService.revoke_member(enterprise, member_id):
        return {"message": "Сотрудник отозван с вашей компании"}
    # raise HTTPEXCEPTION - почитать доку возможно по fastapi.
    return {"message": "Сотрудник не найден или не принадлежит вашей компании"}, 200


@enterprise_router.get('/invite-by-email')
async def invite_by_email(email: str, enterprise: Enterprise = Depends(get_enterprise_by_owner)):
    # try catch - обрабать Exception - HTTPException - то есть что (контент ошибки)
    return await EnterpriseService.invite_by_email(enterprise, email)


@enterprise_router.get('/personal')
async def get_enterprise(enterprise: Enterprise = Depends(get_enterprise_by_owner)):
    try:
        return await EnterpriseService.get(enterprise.id)
    except ServiceException as e:
        return {"message": e.message}