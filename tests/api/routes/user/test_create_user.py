import pytest
from httpx import ASGITransport, AsyncClient

from core.db.session import get_db
from main import app
from tests.conftest import get_test_db, get_user_from_db


@pytest.mark.asyncio
async def test_create_user(test_user, db_session):
    app.dependency_overrides[get_db] = get_test_db
    async with AsyncClient(
        transport=ASGITransport(app), base_url="http://localhost:8000"
    ) as ac:
        resp = await ac.post("/user/", json=test_user)
    data = resp.json()
    assert resp.status_code == 200
    assert data["name"] == test_user["name"]
    assert data["email"] == test_user["email"]
    async for session in get_test_db():
        try:
            user = await get_user_from_db(session, data["user_id"])
            assert user["name"] == test_user["name"]
            assert user["email"] == test_user["email"]
        finally:
            break
