from datetime import datetime

from pydantic import BaseModel


class UserLogin(BaseModel):
    email: str
    password: str


class UserRegister(UserLogin):
    captcha: str


# полное представление о пользователе (/me)
class UserOut(BaseModel):
    email: str
    created_at: datetime
    is_verified: bool
    is_member: bool

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"
    expires_in: int
