from pydantic import BaseModel

from config import settings


class InviteTokenOut(BaseModel):
    tokens: set[str]


class JoinTokenIn(BaseModel):
    inn: str
    token: str


class AccessTokenOut(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 60 * settings.EXPIRES_ACCESS_TOKEN_MINUTES
