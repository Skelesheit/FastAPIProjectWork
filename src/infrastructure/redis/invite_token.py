import secrets

from src.infrastructure.redis import redis

key_token = "referral:tokens:{inn}"


async def create_tokens(inn: str, count: int, nbytes=10) -> set[str]:
    """
    Создаёт токены и кладёт их в Redis
    :param nbytes: количество символов
    :param inn: ИНН компании (к ней токены и относятся)
    :param count: количество токенов
    :return: None
    """
    tokens = {secrets.token_urlsafe(nbytes) for _ in range(count)}
    if not tokens:
        return set()
    key = key_token.format(inn=inn)
    pipe = redis.pipeline(transaction=True)
    redis.set()
    pipe.delete(key)
    pipe.sadd(key, *tokens)
    pipe.expire(key, 24 * 60 * 60)  # 24h
    await pipe.execute()
    return tokens


async def validate_token(inn: str, token: str) -> bool:
    """
    Автоматически проверяет токен и удаляет, если он верный
    удаляется, так как токен должен быть одноразовым
    :param inn: - токены относятся к ИНН компании
    :param token: сам токен (его значение)
    :return: bool - является ли токен валидным или нет
    """
    return await redis.srem(key_token.format(inn=inn), token) == 1


async def get_tokens(inn: str) -> set[str]:
    """
    Возвращает токены, созданные компанией
    :param inn: ИНН компании, к которой привязаны токены
    :return: список доступных токенов компании
    """
    return await redis.smembers(key_token.format(inn=inn))
