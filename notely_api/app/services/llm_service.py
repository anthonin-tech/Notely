import httpx

from app.core.config import settings


class LLMUnavailableError(Exception):
    """Ollama n'est pas joignable."""


class LLMTimeoutError(Exception):
    """Ollama a mis trop de temps à répondre."""


class LLMMalformedResponseError(Exception):
    """La réponse d'Ollama ne contient pas le format attendu."""


async def _call_ollama(messages: list[dict]) -> str:
    payload = {"model": settings.ollama_model, "messages": messages, "stream": False}
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


async def generate_summary(content: str) -> str:
    messages = [{"role": "user", "content": f"Résume ce texte en quelques phrases :\n\n{content}"}]
    return await _call_ollama(messages)


async def generate_chat_reply(messages: list[dict]) -> str:
    return await _call_ollama(messages)
