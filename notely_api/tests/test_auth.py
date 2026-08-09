import pytest

pytestmark = pytest.mark.asyncio(loop_scope="session")


async def test_register_success(client):
    response = await client.post(
        "/register", json={"email": "email@gmail.com", "password": "Fexxxoy01"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "email@gmail.com"


async def test_register_duplicate_email(client):
    await client.post("/register", json={"email": "email@gmail.com", "password": "Fexxxoy01"})
    response = await client.post(
        "/register", json={"email": "email@gmail.com", "password": "Fexxxoy01"}
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "Email déjà utilisé"


async def test_login_wrong_password(client):
    await client.post("/register", json={"email": "email@gmail.com", "password": "Fexxxoy01"})
    response = await client.post(
        "/login", json={"email": "email@gmail.com", "password": "Fexxxoy02"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "email ou mot de passe incorrect"


async def test_login_unknown_email(client):
    response = await client.post(
        "/login", json={"email": "email@gmail.com", "password": "Fexxxoy01"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "email ou mot de passe incorrect"


async def test_me_without_token(client):
    response = await client.get("/me")
    assert response.status_code == 403


async def test_me_with_token(client):
    await client.post("/register", json={"email": "email@gmail.com", "password": "Fexxxoy01"})
    login_response = await client.post(
        "/login", json={"email": "email@gmail.com", "password": "Fexxxoy01"}
    )
    token = login_response.json()["access_token"]
    response = await client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "email@gmail.com"
