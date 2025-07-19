from config import settings
from src.auth import token
from src.clients import captcha, mail
from src.db import models
from src.serializers.user_serializer import UserRegister, UserLogin, UserFillForm
from src.services import ServiceException
from src.use_cases.fill_data_workflow import FillDataWorkflow


class UserService:
    @staticmethod
    async def register(dto: UserRegister) -> dict:
        if not await captcha.verify_yandex_captcha(dto.password, ip='127.0.0.0'):
            raise ServiceException("Капча не пройдёна", 401)
        if await models.User.has_email(dto.email):
            raise ServiceException("Пользователь с таким email уже существует", 401)
        user = await models.User.create(email=dto.email, password=dto.password)
        await mail.send_registration_email(user.id, user.email)
        return {"message": "Пользователь успешно зарегистрирован, проверяйте почту"}

    @staticmethod
    async def login(dto: UserLogin) -> dict:
        invalid_exception = ServiceException("Неправильно введён логин или пароль", 401)
        user = await models.User.get_by_email(dto.email)
        if not user:
            raise invalid_exception
        is_valid = user.check_password(dto.password)
        if not is_valid:
            raise invalid_exception
        refresh_token = await models.RefreshToken.create_by_user_id(user.id)
        access_token = token.generate_access_token(user.id)
        return {"access_token": access_token, "refresh_token" : refresh_token.token, "type": "Bearer", 'expires_in': 60 * settings.EXPIRES_ACCESS_TOKEN_MINUTES}

    @staticmethod
    async def logout(user_id: int) -> dict:
        await models.RefreshToken.delete_by_user_id(user_id)
        return {"message": "Пользователь успешно вышел"}

    @staticmethod
    async def fill_data(dto: UserFillForm, user_id: int) -> dict:
        await FillDataWorkflow.execute(dto, user_id)
        return {"message": "Пользователь успешно заполнил форму о себе"}
