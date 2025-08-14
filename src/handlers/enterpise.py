from fastapi import APIRouter, Depends

from src.auth.dep import get_enterprise_by_owner, get_current_user_id, get_enterprise_inn_by_owner
from src.db.models import Enterprise
from src.serializers.enterprise import EnterpriseFillForm, EnterpriseOut
from src.serializers.token import InviteTokenOut, JoinTokenIn
from src.services.enterprise_service import EnterpriseService

enterprise_router = APIRouter()


@enterprise_router.post("/create")
async def create_enterprise(
        dto: EnterpriseFillForm,
        user_id: int = Depends(get_current_user_id)
) -> EnterpriseOut:
    return await EnterpriseService.create(dto, user_id)


@enterprise_router.get("/generate-tokens/{count}", response_model=InviteTokenOut)
async def generate_tokens(
        count: int,
        inn: str = Depends(get_enterprise_inn_by_owner)
) -> InviteTokenOut:
    tokens = await EnterpriseService.create_invite_token(inn, count)
    return InviteTokenOut(tokens=tokens)


@enterprise_router.post("/join-to-enterprise")
async def join_to_company(
        dto: JoinTokenIn,
        user_id: int = Depends(get_current_user_id)
) -> bool:
    await EnterpriseService.join_by_token(dto, user_id)
    return True


@enterprise_router.get("/revoke/{member_id}")
async def revoke(
        member_id: int,
        enterprise: Enterprise = Depends(get_enterprise_by_owner)
) -> bool:
    return await EnterpriseService.revoke_member(enterprise, member_id)


@enterprise_router.get('/invite-by-email')
def invite_by_email(
        email: str,
        enterprise: Enterprise = Depends(get_enterprise_by_owner)
) -> None:
    # try catch - обрабать Exception - HTTPException - то есть что (контент ошибки)
    EnterpriseService.invite_by_email(enterprise, email)
    return HTTP


@enterprise_router.get('/personal')
async def get_enterprise(
        enterprise: Enterprise = Depends(get_enterprise_by_owner)
) -> EnterpriseOut:
    return await EnterpriseService.get(enterprise.id)
