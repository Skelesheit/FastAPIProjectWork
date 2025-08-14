from fastapi import APIRouter, Response, Security
from fastapi.params import Depends
from starlette import status
from starlette.responses import JSONResponse

from config import settings
from src.auth.dep import bearer_scheme, get_current_user_id
from src.serializers.user import (
    UserLogin,
    UserRegister,
    UserOut
)
from src.services.user_service import UserService

user_router = APIRouter()


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(dto: UserRegister) -> UserOut:
    return await UserService.register(dto)


@user_router.post("/login")
async def login(dto: UserLogin) -> JSONResponse:
    result = await UserService.login(dto)
    response = JSONResponse(status_code=200, content=result)
    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,  # True — если HTTPS
        samesite="lax",
        path="/",
        max_age=60 * 60 * 24 * settings.EXPIRES_REFRESH_TOKEN_DAYS
    )
    return response


@user_router.get("/logout", dependencies=[Security(bearer_scheme)], )
async def logout(user_id: int = Depends(get_current_user_id)) -> JSONResponse:
    result = await UserService.logout(user_id)
    response = JSONResponse(status_code=200, content=result)
    response.delete_cookie(key="refresh_token", path="/")
    return response
