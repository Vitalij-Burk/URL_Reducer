from unittest.mock import AsyncMock

import pytest

from src.app.decorators.user import check_user_ownership_by_email
from src.app.decorators.user import check_user_ownership_by_id


@pytest.mark.asyncio
async def test_check_user_ownership_by_id(fake_users):
    current_user = fake_users.safe_resp
    mock_guard = AsyncMock()

    class Service:
        def __init__(self):
            self.guard = mock_guard

        @check_user_ownership_by_id
        async def method(self, user_id, current_user):
            return "ok"

    service = Service()
    result = await service.method(current_user.user_id, current_user)
    mock_guard.check_user_ownership_by_id.assert_awaited_once_with(
        current_user.user_id, current_user
    )
    assert result == "ok"


@pytest.mark.asyncio
async def test_check_user_ownership_by_id_value_error():
    mock_guard = AsyncMock()

    class Service:
        def __init__(self):
            self.guard = mock_guard

        @check_user_ownership_by_id
        async def method(self):
            pass

    service = Service()
    with pytest.raises(ValueError):
        await service.method()


@pytest.mark.asyncio
async def test_check_user_ownership_by_email(fake_users):
    current_user = fake_users.safe_resp
    mock_guard = AsyncMock()

    class Service:
        def __init__(self):
            self.guard = mock_guard

        @check_user_ownership_by_email
        async def method(self, email, current_user):
            return "ok"

    service = Service()
    result = await service.method(current_user.email, current_user)
    mock_guard.check_user_ownership_by_email.assert_awaited_once_with(
        current_user.email, current_user
    )
    assert result == "ok"


@pytest.mark.asyncio
async def test_check_user_ownership_by_email_value_error():
    mock_guard = AsyncMock()

    class Service:
        def __init__(self):
            self.guard = mock_guard

        @check_user_ownership_by_email
        async def method(self):
            pass

    service = Service()
    with pytest.raises(ValueError):
        await service.method()
