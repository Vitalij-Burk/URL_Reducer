from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.app.decorators.link import check_user_ownership_by_link_id


@pytest.mark.asyncio
async def test_check_user_ownership_by_link_id(fake_users):
    current_user = fake_users.safe_resp
    link_id = uuid4()
    mock_guard = AsyncMock()

    class Service:
        def __init__(self):
            self.guard = mock_guard

        @check_user_ownership_by_link_id
        async def method(self, link_id, current_user):
            return "ok"

    service = Service()
    result = await service.method(link_id, current_user)
    mock_guard.check_user_ownership_by_link_id.assert_awaited_once_with(
        link_id, current_user
    )
    assert result == "ok"


@pytest.mark.asyncio
async def test_check_user_ownership_by_link_id_value_error():
    mock_guard = AsyncMock()

    class Service:
        def __init__(self):
            self.guard = mock_guard

        @check_user_ownership_by_link_id
        async def method(self):
            pass

    service = Service()
    with pytest.raises(ValueError):
        await service.method()
