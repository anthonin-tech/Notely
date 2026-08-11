import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_create_note_success(client, login):
    token = login.json()["access_token"]
    response = await client.post(
        "/notes",
        json={"title": "test", "content": "test de créer une note"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["content"] == "test de créer une note"


async def test_create_note_without_token(client):
    response = await client.post(
        "/notes", json={"title": "test", "content": "test de créer une note sans token"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authenticated"


async def test_get_note_not_found(client, login):
    token = login.json()["access_token"]
    response = await client.get(
        "/notes/64af0000000000000000abcd", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


async def test_get_note_success(client, login):
    token = login.json()["access_token"]
    note_response = await client.post(
        "/notes",
        json={
            "title": "test",
            "content": "test de créer une note et voir si l'utilisateur est accès à la note",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    note_id = note_response.json()["id"]
    response = await client.get(f"/notes/{note_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


async def test_get_note_other_user_forbidden(client):
    await client.post("/register", json={"email": "userA@gmail.com", "password": "userA"})
    login_response_a = await client.post(
        "/login", json={"email": "userA@gmail.com", "password": "userA"}
    )
    token_A = login_response_a.json()["access_token"]
    note_response = await client.post(
        "/notes",
        json={
            "title": "test",
            "content": "test de créer une note et d'y accéder avec une nouvelle note",
        },
        headers={"Authorization": f"Bearer {token_A}"},
    )
    note_id = note_response.json()["id"]
    await client.post("/register", json={"email": "userB@gmail.com", "password": "userB"})
    login_response_b = await client.post(
        "/login", json={"email": "userB@gmail.com", "password": "userB"}
    )
    token_B = login_response_b.json()["access_token"]
    response = await client.get(f"/notes/{note_id}", headers={"Authorization": f"Bearer {token_B}"})
    assert response.status_code == 403


async def test_update_note_partial(client, login):
    token = login.json()["access_token"]
    note_response = await client.post(
        "/notes",
        json={"title": "test", "content": "test pour voir si les modifications fonctionne"},
        headers={"Authorization": f"Bearer {token}"},
    )
    note_id = note_response.json()["id"]
    response = await client.put(
        f"/notes/{note_id}",
        json={"title": "test modifié"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "test modifié"
    assert response.json()["content"] == "test pour voir si les modifications fonctionne"


async def test_delete_note_success(client, login):
    token = login.json()["access_token"]
    note_response = await client.post(
        "/notes",
        json={
            "title": "test",
            "content": "test pour vérifier que les notes se supprimment correctemment",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    note_id = note_response.json()["id"]
    response_delete = await client.delete(
        f"/notes/{note_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response_delete.status_code == 204
    response_get = await client.get(
        f"/notes/{note_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response_get.status_code == 404
