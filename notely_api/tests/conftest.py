import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.db.mongodb import init_db
from app.main import app
from app.models.note import Note
from app.models.user import User


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    settings.mongo_db_name = "notely_test"
    await init_db()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
async def clean_db():
    yield
    await User.delete_all()
    await Note.delete_all()


@pytest.fixture
async def register(client):
    response = await client.post(
        "/register", json={"email": "email@gmail.com", "password": "Fexxxoy01"}
    )
    return response


@pytest.fixture
async def login(client, register):
    response = await client.post(
        "/login", json={"email": "email@gmail.com", "password": "Fexxxoy01"}
    )
    return response
