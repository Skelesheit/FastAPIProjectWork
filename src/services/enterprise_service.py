from src.auth.token import validate_join_email_token
from src.clients.mail import send_invite_email
from src.db.models import User
from src.db.models.enterprise import Enterprise, EnterpriseMember
from src.infrastructure.redis import invite_token
from src.serializers.enterprise import EnterpriseFillForm, EnterpriseOut
from src.serializers.token import JoinTokenIn
from src.services import ServiceException
from src.use_cases.fill_data_workflow import FillDataWorkflow
from src.use_cases.join_employee_workflow import JoinEmployeeWorkflow


class EnterpriseService:
    @staticmethod
    async def create(dto: EnterpriseFillForm, user_id: int) -> dict:
        """
        Создание компании с полным заполнением всех полей
        :param dto: данные с сериализатора, все нужные формы для создания
        :param user_id: id пользователя, будет owner_id
        :return: dict
        """
        await FillDataWorkflow.execute(dto, user_id)
        return {"message": "Пользователь успешно заполнил форму о себе"}

    @staticmethod
    async def get(enterprise_id: int) -> EnterpriseOut:
        enterprise = await Enterprise.get_all_data(enterprise_id)
        if not enterprise:
            raise ServiceException("Нет компании", status=404)
        return EnterpriseOut.model_validate(enterprise)

    @staticmethod
    async def join_by_token(dto: JoinTokenIn, user_id: int) -> bool:
        """
        Присоединение пользователя по токену
        :param dto: dto с токеном и ИНН
        :param user_id: id пользователя
        :return: сообщение dict
        """
        enterprise: Enterprise = await Enterprise.get_by_inn(dto.inn)
        is_valid = await invite_token.validate_token(enterprise.legal_entity.inn, dto.token)
        if not is_valid:
            raise ServiceException(message="Invalid token", status_code=404)
        await EnterpriseMember.create(enterprise_id=enterprise.id, user_id=user_id)
        return True

    @staticmethod
    async def create_invite_token(inn: str, count: int) -> set[str]:
        """
        Создаём токены связанные с ИНН компании
        :param inn: ИНН компании
        :param count: количество нужных токенов, которые задаёт владелец
        :return:
        """
        return await invite_token.create_tokens(inn, count)

    @staticmethod
    async def revoke_member(enterprise: Enterprise, member_id: int) -> bool:
        return await enterprise.delete_member(member_id)

    @staticmethod
    async def get_invite_tokens(enterprise: Enterprise) -> set[str]:
        """
        Получаем invite token-ы: их делает владелец компании
        :param enterprise: Enterprise - модель ORM - сама кампания
        :return: множество токенов
        """
        return await invite_token.get_tokens(enterprise.legal_entity.inn)

    @staticmethod
    async def invite_by_email(enterprise: Enterprise, email: str) -> dict:
        """
        Приглашение сотрудника по email
        :param enterprise:
        :param email: email сотрудника
        :return: None
        """
        await send_invite_email(enterprise.id, email)
        return {"message": "email сообщение отправлено"}

    @staticmethod
    async def join_by_email(token: str) -> dict:
        """
        Приглашение сотрудника по email
        Для этого специальный workflow чтобы было через одну транзакцию
        :param token: токен с email сотрудника и id компании
        :return: dict - сообщение
        """
        enterprise_id, email = validate_join_email_token(token)
        print(enterprise_id, email)
        return await JoinEmployeeWorkflow.execute(enterprise_id, email)
