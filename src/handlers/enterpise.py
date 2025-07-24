from fastapi import APIRouter, Depends, HTTPException

from src.auth.dep import get_enterprise_by_owner, get_current_user_id
from src.db.models import EnterpriseType, Enterprise
from src.serializers.token import InviteTokenOut, JoinTokenIn
from src.serializers.enterprise import EnterpriseFillForm
from src.services.enterprise_service import EnterpriseService

enterprise_router = APIRouter()

@enterprise_router.post("/create")
async def create_enterprise(dto: EnterpriseFillForm, user_id: int = Depends(get_current_user_id)):
    return await EnterpriseService.create(dto, user_id)

@enterprise_router.get("/generate-tokens/{count}", response_model=InviteTokenOut)
async def generate_tokens(count: int, enterprise: EnterpriseType = Depends(get_enterprise_by_owner)):
    tokens = await EnterpriseService.create_invite_token(enterprise, count)
    return InviteTokenOut(tokens=tokens)


@enterprise_router.post("/join-to-company")
async def join_to_company(dto: JoinTokenIn, user_id: int = Depends(get_current_user_id)):
    is_invited = await EnterpriseService.join_by_token(dto, user_id)
    if not is_invited:
        raise HTTPException(status_code=404, detail="Invalid token")
    return {"message": "Пользователь успешно присоединён"}


@enterprise_router.get('/invite-by-email')
async def invite_by_email(email: str, enterprise: Enterprise = Depends(get_enterprise_by_owner)):
    return await EnterpriseService.invite_by_email(enterprise, email)


@enterprise_router.get('/personal')
async def get_enterprise(enterprise: Enterprise = Depends(get_enterprise_by_owner)):
    return await EnterpriseService.get(enterprise.id)
