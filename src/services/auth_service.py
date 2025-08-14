from config import settings
from src.auth import token
from src.db import models
from src.serializers.token import AccessTokenOut
from src.serializers.user import UserOut
from src.services.errors import (
    NotFound,
    RefreshTokenExpired,
    RefreshTokenInvalid
)


class AuthService:
    @staticmethod
    async def me(user_id: int) -> UserOut:
        model = await models.User.get_all_data(user_id)
        if model is None:
            raise NotFound()
        return UserOut.model_validate(model)

    @staticmethod
    async def refresh(refresh_token: str) -> AccessTokenOut:
        token_model = await models.RefreshToken.get_by_token(refresh_token)
        if not token_model:
            raise RefreshTokenInvalid()
        if token_model.expired:
            raise RefreshTokenExpired()
        access_token = token.generate_access_token(token_model.user_id)
        return AccessTokenOut(
            access_token=access_token,
            token_type="Bearer",
            expires_in=60 * settings.EXPIRES_ACCESS_TOKEN_MINUTES,
        )
