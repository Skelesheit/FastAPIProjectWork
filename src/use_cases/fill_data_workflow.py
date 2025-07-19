from src.db import get_session
from src.db import models
from src.db.enums import UserType
from src.serializers.user_serializer import UserFillForm
from src.services import ServiceException


class FillDataWorkflow:
    @staticmethod
    async def execute(dto: UserFillForm, user_id: int) -> dict:
        async with get_session() as session:
            # создание контакта
            await models.Contact.create_with_session(session=session, user_id=user_id, **dto.contact.model_dump())
            # присваиваем тип пользователя
            user = await models.User.get_with_session(user_id, session=session)
            await user.update_with_session(user_type=dto.user_type.value, session=session)
            # ветвление по типу
            match dto.user_type:
                case UserType.Individual:
                    await models.IndividualProfile.create_with_session(session=session, user_id=user_id,
                                                                       **dto.fill.model_dump())
                case UserType.LegalEntity:
                    await models.LegalEntity.create_with_session(session=session, user_id=user_id,
                                                                 **dto.fill.model_dump())
                case UserType.LegalEntityProfile:
                    legal = await models.LegalEntity.create_with_session(session=session, user_id=user_id,
                                                                         **dto.fill.model_dump(exclude={"profile"}))
                    await models.LegalEntityProfile.create_with_session(session=session, legal_id=legal.id,
                                                                        **dto.fill.profile.model_dump())
                case _:
                    raise ServiceException("Неизвестный тип пользователя", 403)
        return {"message": "Профиль успешно заполнен"}
