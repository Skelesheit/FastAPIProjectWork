from config import settings
from src.auth import token
from src.clients import captcha, mail
from src.db import models
from src.serializers.user import (
    UserRegister,
    UserLogin,
    LoginResponse,
    UserOut,
)
from src.services.errors import (
    CaptchaNotVerified,
    NotUniqueEmail,
    InvalidCredentials,
    UserNotVerified
)


class UserService:
    @staticmethod
    async def register(dto: UserRegister) -> UserOut:
        if not await captcha.verify_yandex_captcha(dto.captcha, ip='127.0.0.0'):
            raise CaptchaNotVerified()
        if await models.User.has_email(dto.email):
            raise NotUniqueEmail()
        user = await models.User.create(email=dto.email, password=dto.password)
        mail.send_registration_email(user.id, user.email)
        return UserOut.model_validate(user)

    @staticmethod
    async def login(dto: UserLogin) -> LoginResponse:
        user = await models.User.get_by_email(dto.email)
        if not user:
            raise InvalidCredentials()
        is_valid = user.check_password(dto.password)
        if not is_valid:
            raise InvalidCredentials()
        if not user.is_verified:
            # заново отправим письмо, потом ошибку
            mail.send_registration_email(user.id, user.email)
            raise UserNotVerified()
        refresh_token = await models.RefreshToken.create(user.id)
        access_token = token.generate_access_token(user.id)
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token.token,
            type="Bearer",
            expires_in=60 * settings.EXPIRES_ACCESS_TOKEN_MINUTES
        )

    @staticmethod
    async def logout(user_id: int) -> bool:
        await models.RefreshToken.delete_by_user_id(user_id)
        return True
