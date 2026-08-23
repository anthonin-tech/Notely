from app.services.llm_service import LLMUnavailableError
from app.services.llm_service import LLMTimeoutError
from app.services.llm_service import LLMMalformedResponseError

import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_summarize_note_service_unavailable(client, login, mocker):
    token = login.json()["access_token"]
    note_response = await client.post(
        "/notes",
        json={"title": "test", "content": "un texte à résumer"},
        headers={"Authorization": f"Bearer {token}"},
    )
    note_id = note_response.json()["id"]

    mocker.patch("app.routers.notes_router.generate_summary", side_effect=LLMUnavailableError)

    response = await client.post(
        f"/notes/{note_id}/summarize", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 503


async def test_summarize_note_service_timeout(client, login, mocker):
    token = login.json()["access_token"]
    note_response = await client.post(
        "/notes",
        json={"title": "test", "content": "un texte à résumer"},
        headers={"Authorization": f"Bearer {token}"},
    )
    note_id = note_response.json()["id"]

    mocker.patch("app.routers.notes_router.generate_summary", side_effect=LLMTimeoutError)

    response = await client.post(
        f"/notes/{note_id}/summarize", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 504


async def test_summarize_note_service_MalFormedResponseError(client, login, mocker):
    token = login.json()["access_token"]
    note_response = await client.post(
        "/notes",
        json={"title": "test", "content": "un texte à résumer"},
        headers={"Authorization": f"Bearer {token}"},
    )
    note_id = note_response.json()["id"]

    mocker.patch("app.routers.notes_router.generate_summary", side_effect=LLMMalformedResponseError)

    response = await client.post(
        f"/notes/{note_id}/summarize", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 502
