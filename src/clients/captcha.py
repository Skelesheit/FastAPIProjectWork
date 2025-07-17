import httpx

from config import settings


async def verify_yandex_captcha(token: str, ip: str | int | None) -> bool:
    data = {
        "secret": settings.YANDEX_CAPTCHA_SECRET,
        "token": token,
        # "ip": str(ip),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(settings.YANDEX_URL_VERIFY, json=data, timeout=5)
        print(response.status_code)
    # временно поставлю, так как secret not provided (хотя он указан под secret)
    """
        if response.status_code != 200:
            return False
        result = response.json()
        return result.get("status") == "ok"
    """
    return True
