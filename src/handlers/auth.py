from fastapi import APIRouter, Depends, Request

from src.auth import dep
from src.serializers.token import AccessTokenOut
from src.serializers.user import UserOut
from src.services.auth_service import AuthService
from src.services.errors import Unauthorized

auth_router = APIRouter()


@auth_router.get("/me")
async def me(user_id: int = Depends(dep.get_current_user_id)) -> UserOut:
    return await AuthService.me(user_id)


@auth_router.get("/refresh")
async def refresh(request: Request) -> AccessTokenOut:
    refresh_token = request.cookies.get("refresh_token", None)
    if not refresh_token:
        raise Unauthorized()
    return await AuthService.refresh(refresh_token)
