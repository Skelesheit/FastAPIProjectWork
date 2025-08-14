from src.db import get_session, models
from src.db.enums import EnterpriseType, MemberRole, MemberStatus
from src.serializers.enterprise import EnterpriseFillForm
from src.services.errors import (
    UserAlreadyInEnterprise,
    ValidationFailed,
    UnknownUserType
)


class FillDataWorkflow:
    @staticmethod
    async def execute(dto: EnterpriseFillForm, user_id: int) -> models.Enterprise:
        async with get_session() as session:
            # ну да, надо получить юзера
            user = await models.User.get_with_session(session, user_id)
            if user.is_member:
                raise UserAlreadyInEnterprise
            # основа всего - создание компании
            enterprise = await models.Enterprise.create_with_session(
                session,
                owner_id=user.id,
                name=dto.name,
                enterprise_type=dto.enterprise_type
            )
            # создаём привязку юзера к компании
            await models.EnterpriseMember.create_with_session(
                session,
                user_id=user.id,
                enterprise_id=enterprise.id,
                role=MemberRole.OWNER,
                status=MemberStatus.ACTIVE,
            )
            # ставим юзеру поле, что он теперь member
            # TODO: убрать is_member, теперь можно просто оставлять данные в EnterpriseMember
            await user.update_with_session(session, is_member=True)
            # создание контакта
            await models.Contact.create_with_session(
                session,
                enterprise_id=enterprise.id,
                **dto.contact.model_dump()
            )
            # ветвление по типу - заполнение данных о компании (ИНН ОГРН и прочее)
            match dto.enterprise_type:
                case EnterpriseType.Individual:
                    await models.IndividualProfile.create_with_session(
                        session=session,
                        enterprise_id=enterprise.id,
                        **dto.fill.model_dump()
                    )
                case EnterpriseType.LegalEntity:
                    await models.LegalEntity.create_with_session(
                        session=session,
                        enterprise_id=enterprise.id,
                        **dto.fill.model_dump()
                    )
                case EnterpriseType.LegalEntityProfile:
                    legal_entity = dto.fill
                    legal_entity_profile = legal_entity.legal_entity_profile
                    legal_entity.legal_entity_profile = None
                    if legal_entity is None:
                        raise ValidationFailed(message="not provided legal entity")
                    if legal_entity_profile is None:
                        raise ValidationFailed(message="not provided legal entity profile")
                    legal = await models.LegalEntity.create_with_session(
                        session=session,
                        enterprise_id=enterprise.id,
                        **legal_entity.model_dump()
                    )
                    await models.LegalEntityProfile.create_with_session(
                        session=session,
                        legal_id=legal.id,
                        **legal_entity_profile.model_dump()
                    )
                case _:
                    raise UnknownUserType()
        return enterprise
