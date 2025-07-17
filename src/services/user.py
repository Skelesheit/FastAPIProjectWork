from src.auth import token
from src.db.models import User, RefreshToken
from src.serializers.user import UserRegister, UserLogin, UserOut
from src.clients import captcha, mail
from src.services import ServiceException


class UserService:
    @staticmethod
    async def register(dto: UserRegister) -> dict:
        if not await captcha.verify_yandex_captcha(dto.password):
            raise ServiceException("Капча не пройдёна", 402)
        if await User.has_email(dto.email):
            raise ServiceException("Пользователь с таким email уже существует", 402)
        user = await User.create(email=dto.email, password=dto.password)
        await mail.send_registration_email(user.id, user.email)
        return {"message": "Пользователь успешно зарегистрирован, проверяйте почту"}

    @staticmethod
    async def login(dto: UserLogin) -> dict:
        invalid_exception = ServiceException("Неправильно введён логин или пароль", 403)
        user = await User.get_by_email(dto.email)
        if not user:
            raise invalid_exception
        is_valid = await user.check_password(dto.password)
        if not is_valid:
            raise invalid_exception
        refresh_token = await RefreshToken.create(user.id)
        access_token = token.generate_access_token(user.id)
        return {"access_token": access_token, "refresh_token": refresh_token}

    @staticmethod
    async def logout(refresh_token: str) -> dict:
        await RefreshToken.delete_by_token(refresh_token)
        return {"message": "Польватель успешно вышел"}


