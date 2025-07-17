import httpx

from config import settings

async def suggest_company_by_inn(query: str) -> dict | None:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Token {settings.DADATA_TOKEN}"
    }
    body = {"query": query}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.DADATA_API_URL,
            headers=headers,
            json=body
        )
    suggestions = response.json().get("suggestions", [])
    return suggestions[0]["data"] if suggestions else None
