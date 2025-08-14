# translators.py — перевод PyJWT -> доменные
from contextlib import contextmanager
from jwt import ExpiredSignatureError, InvalidTokenError

@contextmanager
def translate_token_errors(*, invalid_exc, expired_exc):
    try:
        yield
    except ExpiredSignatureError as e:
        raise expired_exc() from e
    except (InvalidTokenError, KeyError, TypeError, ValueError) as e:
        raise invalid_exc() from e
