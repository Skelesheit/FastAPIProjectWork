from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from src.auth.token import validate_token
from src.db.models import Enterprise, EnterpriseMember

bearer_scheme = HTTPBearer()


def get_current_user_id(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> int:
    token = credentials.credentials
    print(token)
    try:
        user_id = validate_token(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    return user_id


async def get_enterprise_by_user_id(user_id: int = Depends(get_current_user_id)) -> int:
    enterprise_id = await EnterpriseMember.get_enterprise_id_by_user_id(user_id)
    if not enterprise_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    return enterprise_id


async def get_enterprise_by_owner(user_id: int = Depends(get_current_user_id)) -> Enterprise:
    enterprise = await Enterprise.get_enterprise_by_owner(user_id)
    if not enterprise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="компания не найдена")
    return enterprise


async def get_enterprise_inn_by_owner(user_id: int = Depends(get_current_user_id)) -> str:
    inn = await Enterprise.get_enterprise_inn_by_owner(user_id)
    if not inn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="компания не найдена")
    return inn
