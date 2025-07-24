from src.auth.token import generate_join_token
from src.infrastructure.redis import redis


async def create_tokens(inn: str, count: int) -> set[str]:
    """
    Создаёт токены и кладёт их в Redis
    :param inn: ИНН компании (к ней токены и относятся)
    :param count: количество токенов
    :return: None
    """
    tokens = {generate_join_token() for _ in range(count)}
    key = f"tokens:{inn}"
    await redis.sadd(key, *tokens)
    await redis.expire(key, 60 * 60 * 24)  # TTL в 24 часа
    return tokens


async def validate_token(inn: str, token: str) -> bool:
    """
    Автоматически проверяет токен и удаляет, если он верный
    удаляется, так как токен должен быть одноразовым
    :param inn: - токены относятся к ИНН компании
    :param token: сам токен (его значение)
    :return: bool - является ли токен валидным или нет
    """
    key = f"tokens:{inn}"
    exists = await redis.sismember(key, token)
    if not exists:
        return False
    await redis.srem(key, token)
    return True


async def get_tokens(inn: str) -> set[str]:
    """
    Возвращает токены, созданные компанией
    :param inn: ИНН компании, к которой привязаны токены
    :return: список доступных токенов компании
    """
    return await redis.smembers(f"tokens:{inn}")
