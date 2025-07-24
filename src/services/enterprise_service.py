from src.auth.token import validate_join_token
from src.clients.mail import send_invite_email
from src.db.models import User
from src.db.models.enterprise import Enterprise, EnterpriseMember
from src.infrastructure.redis import invite_token
from src.serializers.enterprise import EnterpriseFillForm, EnterpriseOut
from src.serializers.token import JoinTokenIn
from src.services import ServiceException
from src.use_cases.fill_data_workflow import FillDataWorkflow


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
    async def create_invite_token(enterprise: Enterprise, count: int) -> set[str]:
        """
        Создаём токены связанные с ИНН компании
        :param enterprise: ORM модель Enterprise
        :param count: количество нужных токенов, которые задаёт владелец
        :return:
        """
        return await invite_token.create_tokens(enterprise.legal_entity.inn, count)

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
        :param token: токен
        :param email: email сотрудника
        :return: dict - сообщение
        """
        enterprise_id, email = validate_join_token(token)
        user = await User.get_by_email(email)
        if not user:
            raise ServiceException("Пользователь ещё не зарегистрирован и не верифицирован", 404)
        if not user.is_verified:
            raise ServiceException("Пользователь не верифицирован", 400)
        await EnterpriseMember.create(enterprise_id=enterprise_id, user_id=user.id)
        return {"message": "Пользователь успешно присоединён к компании"}
