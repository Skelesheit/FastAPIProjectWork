from src.db import enums
from src.db import get_session
from src.db import models
from src.services.errors import (
    UserNotRegistered,
    UserNotVerified,
    UserAlreadyInEnterprise
)


class JoinEmployeeWorkflow:
    @staticmethod
    async def execute(enterprise_id: int, email: str) -> models.EnterpriseMember:
        async with get_session() as session:
            user = await models.User.get_by_email_with_session(session, email=email)
            if not user:
                raise UserNotRegistered()
            if not user.is_verified:
                raise UserNotVerified()
            if await models.EnterpriseMember.has_email_with_session(session, user.email):
                raise UserAlreadyInEnterprise()
            # теперь он тоже member
            await user.update_with_session(session, is_member=True)
            # создание связи пользователя к компании
            return await models.EnterpriseMember.create_with_session(
                session,
                enterprise_id=enterprise_id,
                user_id=user.id,
                role=enums.MemberRole.EMPLOYEE,
                status=enums.MemberStatus.ACTIVE,
            )
