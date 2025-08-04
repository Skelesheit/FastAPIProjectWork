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
    await redis.set(key_token.format(inn=inn), *tokens, ex=60 * 60 * 24)
    return tokens


async def validate_token(inn: str, token: str) -> bool:
    """
    Автоматически проверяет токен и удаляет, если он верный
    удаляется, так как токен должен быть одноразовым
    :param inn: - токены относятся к ИНН компании
    :param token: сам токен (его значение)
    :return: bool - является ли токен валидным или нет
    """
    if not await redis.sismember(key_token.format(inn=inn), token):
        return False
    return await redis.srem(key_token.format(inn=inn), token)


async def get_tokens(inn: str) -> set[str]:
    """
    Возвращает токены, созданные компанией
    :param inn: ИНН компании, к которой привязаны токены
    :return: список доступных токенов компании
    """
    return await redis.smembers(key_token.format(inn=inn))
