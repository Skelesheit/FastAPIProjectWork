from pydantic import ValidationError

from src.auth import token
from src.db import models
from src.serializers.user import UserOut
from src.services import ServiceException


class AuthService:
    @staticmethod
    async def me(user_id: int) -> UserOut:
        model = await models.User.get_all_data(user_id)
        if model is None:
            raise ServiceException("User not found", 404)
        try:
            return UserOut.model_validate(model)
        except ValidationError as e:
            raise ServiceException(e, 400)

    @staticmethod
    async def refresh(refresh_token: str) -> dict:
        print(refresh_token)
        token_model = await models.RefreshToken.get_by_token(refresh_token)
        if not token_model:
            raise ServiceException("Invalid refresh token", 404)
        if token_model.expired:
            raise ServiceException("Refresh token expired", 401)
        access_token = token.generate_access_token(token_model.user_id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token, #TODO:"deprecated"
            "type": "Bearer",
        }
