import pytest
from httpx import AsyncClient, ASGITransport
from http import HTTPStatus
from users.presentation.models import UserCreate, UserRead, UserUpdate

from main import app
from core.config import settings

transport = ASGITransport(app=app)

@pytest.fixture
async def client():
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as c:
        yield c

@pytest.fixture
async def new_user(client):
    payload = {
        "last_name":   "Петров",
        "first_name":  "Пётр",
        "middle_name": "Петрович"
    }
    resp = await client.post("/users/", json=payload)
    assert resp.status_code == HTTPStatus.CREATED

    user = UserRead(**resp.json())
    return user
