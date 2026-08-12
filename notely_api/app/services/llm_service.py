import httpx

from app.core.config import settings


class LLMUnavailableError(Exception):
    """Ollama n'est pas joignable."""


class LLMTimeoutError(Exception):
    """Ollama a mis trop de temps à répondre."""


class LLMMalformedResponseError(Exception):
    """La réponse d'Ollama ne contient pas le format attendu."""


async def generate_summary(content: str) -> str:
    payload = {
        "model": settings.ollama_model,
        "messages": [
            {"role": "user", "content": f"Résume ce texte en quelques phrases: \n\n{content}"}
        ],
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        try:
            response = await client.post(f"{settings.ollama_base_url}/api/chat", json=payload)

        except httpx.ConnectError:
            raise LLMUnavailableError
        except httpx.TimeoutException:
            raise LLMTimeoutError
        try:
            return response.json()["message"]["content"]
        except KeyError:
            raise LLMMalformedResponseError("Réponse malformée")
