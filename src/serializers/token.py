from pydantic import BaseModel


class InviteTokenOut(BaseModel):
    tokens: set[str]


class JoinTokenIn(BaseModel):
    inn: str
    token: str