from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth.token import validate_token
from src.db import models

security = HTTPBearer()


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # вся суть в получении пользователя
        request.state.user = None
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)
        token = auth_header.split(" ")[1]
        try:
            user_id = validate_token(token)
        except Exception as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})
        # Получаем пользователя и кладём в request.state
        user = await models.User.get(user_id)
        if user is None:
            return JSONResponse(status_code=401, content={"detail": "User not found"})
        request.state.user = user
        return await call_next(request)


class VerifiedUser:
    async def __call__(
            self,
            creds: HTTPAuthorizationCredentials = Depends(security),
            request: Request = None,
    ):
        token = creds.credentials
        user = getattr(request.state, "user", None)
        if not user:
            user_id = validate_token(token)
            user = await models.User.get_by_id(user_id)
            if not user:
                raise HTTPException(status_code=401, detail="Unauthorized")
        if not user.is_verified:
            raise HTTPException(status_code=403, detail="User not verified")
        return user
