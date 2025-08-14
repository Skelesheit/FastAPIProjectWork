from src.auth.token import validate_join_email_token
from src.clients.mail import send_invite_email
from src.db.enums import EnterpriseType
from src.db.models.enterprise import Enterprise, EnterpriseMember
from src.infrastructure.redis import invite_token
from src.serializers.enterprise import EnterpriseFillForm, EnterpriseOut
from src.serializers.token import JoinTokenIn
from src.services.errors import (
    EnterpriseNotFound,
    JoinTokenError,
    InviteByInnNotAllowedForIndividuals, JoinTokenInvalid, JoinTokenExpired
)
from src.services.translators import translate_token_errors
from src.use_cases import FillDataWorkflow, JoinEmployeeWorkflow


class EnterpriseService:
    @staticmethod
    async def create(dto: EnterpriseFillForm, user_id: int) -> EnterpriseOut:
        """
        Создание компании с полным заполнением всех полей
        :param dto: данные с сериализатора, все нужные формы для создания
        :param user_id: id пользователя, будет owner_id
        :return: dict
        """
        # TODO: Надо убрать is_member - и всё заменить на поиск в EnterpriseMember
        model =  await FillDataWorkflow.execute(dto, user_id)
        return EnterpriseOut.from_model(model)

    @staticmethod
    async def get(enterprise_id: int) -> EnterpriseOut:
        enterprise = await Enterprise.get_all_data(enterprise_id)
        if not enterprise:
            raise EnterpriseNotFound()
        return EnterpriseOut.model_validate(enterprise)

    @staticmethod
    async def join_by_token(dto: JoinTokenIn, user_id: int) -> EnterpriseMember:
        """
        Присоединение пользователя по токену
        :param dto: dto с токеном и ИНН
        :param user_id: id пользователя
        :return: сообщение dict
        """
        enterprise: Enterprise = await Enterprise.get_by_inn(dto.inn)
        if not enterprise:
            raise EnterpriseNotFound()
        if enterprise.enterprise_type == EnterpriseType.Individual:
            raise InviteByInnNotAllowedForIndividuals()
        if not await invite_token.validate_token(enterprise.legal_entity.inn, dto.token):
            raise JoinTokenError()
        return await EnterpriseMember.create(enterprise_id=enterprise.id, user_id=user_id)

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
    def invite_by_email(enterprise: Enterprise, email: str) -> None:
        """
        Приглашение сотрудника по email
        :param enterprise:
        :param email: email сотрудника
        :return: None
        """
        send_invite_email(enterprise.id, email)

    @staticmethod
    async def join_by_email(token: str) -> EnterpriseMember:
        """
        Приглашение сотрудника по email
        Для этого специальный workflow чтобы было через одну транзакцию
        :param token: токен с email сотрудника и id компании
        :return: dict - сообщение
        """
        with translate_token_errors(invalid_exc=JoinTokenInvalid, expired_exc=JoinTokenExpired):
            # -> {"enterprise_id": ..., "email": ...}
            args = validate_join_email_token(token)
        return await JoinEmployeeWorkflow.execute(**args)
