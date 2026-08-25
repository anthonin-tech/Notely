from app.services.llm_service import LLMUnavailableError
from app.services.llm_service import LLMTimeoutError
from app.services.llm_service import LLMMalformedResponseError

import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")

async def test_chat_service_unavaible(client, login, mocker):
    token = login.json()["access_token"]

    mocker.patch("app.routers.chatbot_router.generate_chat_reply", side_effect=LLMUnavailableError)

    response = await client.post(
        "/chat",
        json={"content": "salut"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 503

async def test_chat_service_timeout(client, login, mocker):
    token = login.json()["access_token"]

    mocker.patch("app.routers.chatbot_router.generate_chat_reply", side_effect=LLMTimeoutError)

    response = await client.post(
        "/chat",
        json={"content": "salut"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 504

async def test_chat_malformed_response(client, login, mocker):
    token = login.json()["access_token"]

    mocker.patch("app.routers.chatbot_router.generate_chat_reply", side_effect=LLMMalformedResponseError)

    response = await client.post(
        "/chat",
        json={"content": "salut"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 502