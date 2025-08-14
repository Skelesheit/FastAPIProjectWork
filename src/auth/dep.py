from typing import Annotated

from fastapi import Depends, HTTPException, Request, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from src.auth.token import validate_token
from src.db.models import Enterprise, EnterpriseMember

bearer_scheme = HTTPBearer(auto_error=False)  # не кидает сам, даёт нам решить


def get_current_user_id(
        request: Request,
        credentials: Annotated[HTTPAuthorizationCredentials | None, Security(bearer_scheme)],
) -> int:
    if credentials is None:
        # нет токена
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    try:
        user_id = validate_token(token)  # должен вернуть int и кидать PyJWT-исключения если токен битый/просрочен
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # на случай если validate_token возвращает None
    if not isinstance(user_id, int):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    request.state.user_id = user_id
    return user_id


company_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="company not found"
)


async def get_enterprise_by_user_id(
        request: Request,
        user_id: int = Depends(get_current_user_id)
) -> int:
    enterprise_id = await EnterpriseMember.get_enterprise_id_by_user_id(user_id)
    if not enterprise_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is not a member of any enterprise"
        )
    request.state.enterprise_id = enterprise_id
    return enterprise_id


async def get_enterprise_by_owner(
        request: Request,
        user_id: int = Depends(get_current_user_id)
) -> Enterprise:
    enterprise = await Enterprise.get_enterprise_by_owner(user_id)
    if not enterprise:
        raise company_not_found_exception
    request.state.enterprise_id = enterprise.id
    return enterprise


async def get_enterprise_inn_by_owner(
        user_id: int = Depends(get_current_user_id)
) -> str:
    inn = await Enterprise.get_enterprise_inn_by_owner(user_id)
    if not inn:
        raise company_not_found_exception
    return inn
