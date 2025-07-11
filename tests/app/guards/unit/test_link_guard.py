from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.app.guards.link import LinkGuard
from src.core.domain.http_errors import ForbiddenError
from src.core.domain.schemas.safe.link import LinkResponse


@pytest.mark.asyncio
async def test_check_user_ownership_by_link_id_success(fake_users):
    link_id = uuid4()
    current_user = fake_users.safe
    mock_link_manager = AsyncMock()
    guard = LinkGuard(mock_link_manager)
    mock_link_manager.get_by_id.return_value = LinkResponse(
        link_id=link_id,
        user_id=current_user.user_id,
        name="test",
        entry_link="https://yt.com",
        short_link="fsasdD23",
        clicks=1,
    )

    result = await guard.check_user_ownership_by_link_id(link_id, current_user)

    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_link_id_forbidden(fake_users):
    link_id = uuid4()
    current_user = fake_users.safe
    mock_link_manager = AsyncMock()
    guard = LinkGuard(mock_link_manager)
    mock_link_manager.get_by_id.return_value = LinkResponse(
        link_id=link_id,
        user_id=uuid4(),
        name="test",
        entry_link="https://yt.com",
        short_link="fsasdD23",
        clicks=1,
    )

    with pytest.raises(ForbiddenError):
        await guard.check_user_ownership_by_link_id(link_id, current_user)
