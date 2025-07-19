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
    secret_key = settings.SECRET_KEY
    print("secret on generate:", secret_key)
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    print("token by generate:", token)
    return token


def validate_token(token: str) -> int | None:
    try:
        secret_key = settings.SECRET_KEY
        print("secret on validate:", secret_key)
        print(f"settings.secret_key = {settings.SECRET_KEY!r}")
        print("token by validate:", token)
        print(f"Token raw: {repr(token)}")
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
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