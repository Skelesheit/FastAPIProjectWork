from fastapi import APIRouter, Depends, Request, Security, HTTPException
from starlette.responses import JSONResponse

from config import settings
from src.auth import dep
from src.auth.dep import bearer_scheme
from src.serializers.user import UserOut
from src.services import ServiceException
from src.services.auth_service import AuthService

auth_router = APIRouter()


@auth_router.get("/me", dependencies=[Security(bearer_scheme)], response_model=UserOut)
async def me(user_id: int = Depends(dep.get_current_user_id)):
    try:
        return await AuthService.me(user_id)
    except ServiceException as e:
        return JSONResponse(content=e.json_message, status_code=e.status_code)


@auth_router.get("/refresh")
async def refresh(request: Request) -> JSONResponse:
    refresh_token = request.cookies.get("refresh_token", None)
    if not refresh_token:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        tokens = await AuthService.refresh(refresh_token)
    except ServiceException as e:
        return JSONResponse(content=e.json_message, status_code=e.status_code)
    message = {
        'access_token': tokens['access_token'],
        'type': tokens['type'],
        'expires_in': 60 * settings.EXPIRES_ACCESS_TOKEN_MINUTES,
    }
    response = JSONResponse(content=message, status_code=200)
    response.headers["Authorization"] = f"{tokens["type"]} {tokens['access_token']}"
    print('refresh_token:', tokens['refresh_token'])
    response.set_cookie(
        key='refresh_token',
        value=tokens['refresh_token'],
        httponly=True,
        secure=False,
        samesite='lax',
        path='/',
        max_age=60 * 60 * 24 * settings.EXPIRES_REFRESH_TOKEN_DAYS
    )
    return response
