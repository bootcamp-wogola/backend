import pytest

from app.core.security import get_password_hash
from app.modules.user.models import User, UserRole



async def create_user(session, *, username, email, password, role=UserRole.USER):
    user = User(
        username=username,
        email=email,
        password=get_password_hash(password),
        role=role,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_token(client, email, password):
    response = await client.post(
        "/api/v1/auth/token",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_and_read_user(client):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret",
        "role": "user",
    }

    response = await client.post("/api/v1/users/", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == payload["username"]
    assert body["email"] == payload["email"]
    assert body["role"] == payload["role"]

    user_id = body["id"]
    get_response = await client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == user_id


@pytest.mark.asyncio
async def test_create_user_conflict(client):
    payload = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "secret",
        "role": "user",
    }
    response = await client.post("/api/v1/users/", json=payload)
    assert response.status_code == 201

    conflict_response = await client.post("/api/v1/users/", json=payload)
    assert conflict_response.status_code == 409


@pytest.mark.asyncio
async def test_update_user_self_only(client, db_session):
    user = await create_user(
        db_session,
        username="self",
        email="self@example.com",
        password="secret",
    )
    other_user = await create_user(
        db_session,
        username="other",
        email="other@example.com",
        password="secret",
    )

    token = await get_token(client, user.email, "secret")
    headers = {"Authorization": f"Bearer {token}"}

    update_response = await client.patch(
        f"/api/v1/users/{user.id}",
        json={"username": "self-updated"},
        headers=headers,
    )
    assert update_response.status_code == 200
    assert update_response.json()["username"] == "self-updated"

    forbidden_response = await client.patch(
        f"/api/v1/users/{other_user.id}",
        json={"username": "nope"},
        headers=headers,
    )
    assert forbidden_response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user_self_only(client, db_session):
    user = await create_user(
        db_session,
        username="delete",
        email="delete@example.com",
        password="secret",
    )

    token = await get_token(client, user.email, "secret")
    headers = {"Authorization": f"Bearer {token}"}

    delete_response = await client.delete(
        f"/api/v1/users/{user.id}",
        headers=headers,
    )
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/users/{user.id}")
    assert get_response.status_code == 404
