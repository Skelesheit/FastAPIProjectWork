from fastapi import APIRouter
from starlette.responses import Response

from src.serializers.user import UserLogin, UserRegister, UserFillForm

user_router = APIRouter()

@user_router.post("/register")
async def register(request: UserRegister) -> Response:
    pass

@user_router.post("/login")
async def login(request: UserLogin) -> Response:
    pass

@user_router.get("/logout")
async def logout() -> Response:
    pass

@user_router.post("/fill")
async def fill(request: UserFillForm) -> Response:
    pass