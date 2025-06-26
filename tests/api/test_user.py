from http import HTTPStatus
import pytest
from users.models import UserRead, UserCreate, UserUpdate

@pytest.mark.parametrize("payload", [
    {"last_name": "Иванов", "first_name": "Иван", "middle_name": "Иванович"},
    {"last_name": "Ниикта", "first_name": "НИк"}
])
async def test_create(client, payload):

    user = UserCreate(**payload)
    assert isinstance(user, UserCreate)

    response = await client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()
    user = UserRead(**data)

    assert user.last_name == payload["last_name"]
    assert user.first_name == payload["first_name"]
    assert hasattr(user, "id")


async def test_get(client, new_user):
    response = await client.get(f"/users/{new_user.id}")
    assert response.status_code == HTTPStatus.OK

    user = UserRead(**response.json())
    assert user.id == new_user.id

@pytest.mark.parametrize("payload",[
    {"last_name": "1", "first_name":"2", "middle_name":"3"},
    {"last_name": "1", "middle_name":"3"},
    {"middle_name":"3"},
])
async def test_update(client, new_user, payload):
    user_data = UserUpdate(**payload)
    assert isinstance(user_data, UserUpdate)

    response = await client.patch(f"/users/{new_user.id}", json=payload)
    assert response.status_code == HTTPStatus.OK


async def test_delete(client, new_user):
    response = await client.delete(f"/users/{new_user.id}")
    assert response.status_code == HTTPStatus.OK

    error_response = await client.delete(f"/users/{new_user.id}")
    assert error_response.status_code == HTTPStatus.NOT_FOUND
