import pytest

<<<<<<< HEAD
from app.core.security import get_password_hash
from app.modules.user.models import User, UserRole
=======
from src.core.security import get_password_hash
from src.modules.user.model import User, UserRole
>>>>>>> b5272105049f09718847e2199ccf71caed8f8ae7


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


@pytest.mark.asyncio
async def test_token_success_and_failure(client, db_session):
    user = await create_user(
        db_session,
        username="tokenuser",
        email="token@example.com",
        password="secret",
    )

    response = await client.post(
        "/api/v1/auth/token",
        data={"username": user.email, "password": "secret"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]

    bad_response = await client.post(
        "/api/v1/auth/token",
        data={"username": user.email, "password": "wrong"},
    )
    assert bad_response.status_code == 401
