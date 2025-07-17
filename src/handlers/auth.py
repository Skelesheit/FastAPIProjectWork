from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from src.serializers.user import UserOut

auth_router = APIRouter()

@auth_router.get("/me", response_model=UserOut)
async def login():
    pass

@auth_router.get("/refresh")
async def refresh():
    pass