import secrets
import string
from datetime import datetime, timedelta, timezone

import jwt

from config import settings


def generate_access_token(_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'exp': now + timedelta(minutes=settings.EXPIRES_ACCESS_TOKEN_MINUTES),
        'iat': now,
        'sub': str(_id),
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

def generate_join_email_token(enterprise_id: int, email: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'exp': now + timedelta(hours=24),
        'iat': now,
        'id': str(enterprise_id),
        'email': email,
        'type': 'join'
    }
    secret_key = settings.SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def validate_join_email_token(token: str) -> [int, str]:
    try:
        secret_key = settings.SECRET_KEY
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"require": ["exp", "iat", "id", "email", "type"]},
            leeway=10
        )
        if payload.get('type') != 'join':
            raise Exception('Неверный тип токена')
        return int(payload['id']), payload['email']
    except jwt.ExpiredSignatureError:
        raise Exception('Токен истёк')
    except jwt.InvalidTokenError:
        raise Exception('Неверный токен')


def generate_join_token(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))
