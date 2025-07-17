from datetime import datetime, timedelta, timezone

import jwt

from config import settings


def generate_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'exp': now + timedelta(minutes=settings.EXPIRES_ACCESS_TOKEN_MINUTES),
        'iat': now,
        'sub': str(user_id),
        'type': 'access'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def validate_token(token: str) -> int | None:
    try:
        payload = jwt.decode(
            token,
            secret=settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"require": ["exp", "iat", "sub", "type"]},
            leeway=10
        )
        if payload.get('type') != 'access':
            raise Exception('Неверный тип токена')
        return int(payload['sub'])
    except jwt.ExpiredSignatureError:
        raise Exception('Токен истёк')
    except jwt.InvalidTokenError:
        raise Exception('Неверный токен')
