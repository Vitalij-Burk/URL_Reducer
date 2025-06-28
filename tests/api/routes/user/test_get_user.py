import pytest
from httpx import ASGITransport, AsyncClient

from src.core.db.session import get_db
from src.main import app
from tests.conftest import (
    create_access_token_for_test,
    create_user_in_db,
    get_test_db,
)


@pytest.mark.skip
async def test_get_user(test_user, db_session):
    app.dependency_overrides[get_db] = get_test_db
    try:
        async for session in get_test_db():
            try:
                user = await create_user_in_db(session, **test_user)
                assert user["name"] == test_user["name"]
                assert user["email"] == test_user["email"]
                break
            finally:
                pass
        async with AsyncClient(transport=ASGITransport(app), base_url="http://localhost:8000") as ac:
            resp = await ac.get(
                f"/user/id/{user['user_id']}",
                headers=create_access_token_for_test(test_user["email"]),
            )
        data = resp.json()
        assert resp.status_code == 200
        assert data["name"] == test_user["name"]
        assert data["email"] == test_user["email"]
    finally:
        app.dependency_overrides.clear()
