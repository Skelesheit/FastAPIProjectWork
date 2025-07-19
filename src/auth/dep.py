from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from src.auth.token import validate_token

bearer_scheme = HTTPBearer()


def get_current_user_id(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> int:
    token = credentials.credentials.split()[1]
    print(token)
    try:
        user_id = validate_token(token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    return user_id
