from src.auth.token import validate_token
from src.clients import dadata
from src.db.models import User
from src.services.exceptions import ServiceException


class ClientService:
    @staticmethod
    async def suggest_company_by_inn(inn: str) -> dict:
        if inn is None:
            raise ServiceException("ИНН не может быть пустым", 403)
        if not inn.isdigit():
            raise ServiceException("ИНН должен состоять из цифр", 403)
        if len(inn) not in (10, 12):
            raise ServiceException("ИНН должен иметь длину от 10 до 12 цифр", 403)
        suggestion = await dadata.suggest_company_by_inn(inn)
        if not suggestion:
            raise ServiceException("Ничего не найдено", 404)
        # любой внешний сервис может сбоить, ПОЭТОМУ ПРОВЕРКА НА ПОЛНОТУ ДАННЫХ
        return suggestion

    @staticmethod
    async def verify_mail(token: str) -> None:
        user_id = validate_token(token)
        if not user_id:
            raise ServiceException("Invalid email token", 403)
        if not await User.verify_email(user_id):
            raise ServiceException("User not verified", 400)
