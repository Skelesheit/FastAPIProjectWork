from src.auth.token import validate_token
from src.clients import dadata
from src.db.models import User
from src.serializers.clients import DadataOrganization
from src.services.errors import (
    INNMissing,
    INNInvalidLength,
    INNInvalidFormat,
    NotFound,
    EmailConfirmTokenInvalid,
    UserNotVerified
)


class ClientService:
    @staticmethod
    async def suggest_company_by_inn(inn: str) -> DadataOrganization:
        suggestion = await dadata.suggest_company_by_inn(inn)
        if not suggestion:
            raise NotFound()
        return suggestion

    @staticmethod
    async def verify_mail(token: str) -> None:
        user_id = validate_token(token)
        if not user_id:
            raise EmailConfirmTokenInvalid()
        await User.verify_email(user_id)
