from src.auth.token import validate_token
from src.clients import dadata
from src.db.models import User
from src.services.exceptions import ServiceException


class ClientService:
    @staticmethod
    async def suggest_company_by_inn(inn: str) -> dict:
        if not inn.isdigit():
            raise ServiceException("ИНН должен состоять из цифр", 403)
        if len(inn) < 10 or len(inn) > 12:
            raise ServiceException("ИНН должен иметь длину от 10 до 12 цифр", 403)
        suggestion = await dadata.suggest_company_by_inn(inn)
        if not suggestion:
            raise ServiceException("Ничего не найдено", 404)
        return suggestion

    @staticmethod
    async def verify_mail(token: str) -> None:
        user_id = validate_token(token)
        if not user_id:
            raise ServiceException("Invalid email token", 403)
        is_verified = await User.verify_email(user_id)
        if not is_verified:
            raise ServiceException("User not verified. Debug please", 500)
