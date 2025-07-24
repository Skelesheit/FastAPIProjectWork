from src.db import get_session
from src.db import models
from src.db.enums import EnterpriseType
from src.serializers.enterprise import EnterpriseFillForm
from src.services import ServiceException


class FillDataWorkflow:
    @staticmethod
    async def execute(dto: EnterpriseFillForm, user_id: int) -> dict:
        async with get_session() as session:
            # основа всего - создание компании
            enterprise = await models.Enterprise.create_with_session(
                session,
                owner_id=user_id,
                name=dto.name,
                enterprise_type=dto.enterprise_type
            )
            # создание контакта
            await models.Contact.create_with_session(
                session,
                enterprise_id=enterprise.id,
                **dto.contact.model_dump()
            )
            # ветвление по типу
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
                    profile_data = getattr(dto.fill, "profile", None)
                    if not profile_data:
                        raise ServiceException("Отсутствует профиль для юр.лица", 400)
                    legal = await models.LegalEntity.create_with_session(
                        session=session,
                        enterprise_id=enterprise.id,
                        **dto.fill.model_dump(exclude={"profile"})
                    )
                    await models.LegalEntityProfile.create_with_session(
                        session=session,
                        legal_id=legal.id,
                        **dto.fill.profile.model_dump()
                    )
                case _:
                    raise ServiceException("Неизвестный тип пользователя", 403)
        return {"message": "Профиль успешно заполнен"}
