from fastapi import APIRouter, Request, Response, HTTPException, Security
from fastapi.params import Depends
from starlette import status
from starlette.responses import JSONResponse

from config import settings
from src.auth.dep import bearer_scheme, get_current_user_id
from src.serializers.user import UserLogin, UserRegister
from src.services import ServiceException
from src.services.user_service import UserService

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(dto: UserRegister) -> Response:
    try:
        message = await UserService.register(dto)
    except ServiceException as e:
        return JSONResponse(status_code=e.status_code, content=e.json_message)
    return JSONResponse(status_code=200, content=message)


@user_router.post("/login")
async def login(dto: UserLogin) -> JSONResponse:
    try:
        result = await UserService.login(dto)
    except ServiceException as e:
        return JSONResponse(status_code=e.status_code, content=e.json_message)
    message = {
        'access_token': result['access_token'],
        'type': result['type'],
        'expires_in': result['expires_in'],
    }
    response = JSONResponse(status_code=200, content=message)
    response.headers["Authorization"] = f"Bearer {result['access_token']}"
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
async def logout(user_id: int = Depends(get_current_user_id)) -> Response:
    if user_id is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        result = await UserService.logout(user_id)
    except ServiceException as e:
        return JSONResponse(status_code=e.status_code, content=e.json_message)
    response = JSONResponse(status_code=200, content=result)
    response.headers["Authorization"] = ""
    response.delete_cookie(key="refresh_token", path="/")
    return response
