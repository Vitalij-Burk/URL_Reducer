from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.links.app.guards import LinkGuard
from src.links.core.domain.exceptions.link import LinkForbidden
from src.users.core.domain.schemas.inner.user import UserResponseInner


@pytest.mark.asyncio
async def test_check_user_ownership_by_link_id_success(fake_users, fake_links):
    current_user = fake_users.safe_resp
    mock_link_manager = AsyncMock()
    mock_folder_manager = AsyncMock()
    guard = LinkGuard(mock_link_manager, mock_folder_manager)
    mock_link_manager.get_by_id.return_value = fake_links.inner_resp
    result = await guard.check_user_ownership_by_link_id(
        fake_links.safe_resp.link_id, current_user.user_id
    )
    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_link_id_forbidden(fake_links):
    current_user = UserResponseInner(
        user_id=uuid4(),
        name="fasfas",
        email="em@fad.con",
        hashed_password="fafdsafas",
        link_ids=[],
        folder_ids=[],
    )
    mock_link_manager = AsyncMock()
    mock_folder_manager = AsyncMock()
    guard = LinkGuard(mock_link_manager, mock_folder_manager)
    mock_link_manager.get_by_id.return_value = fake_links.inner_resp
    with pytest.raises(LinkForbidden):
        await guard.check_user_ownership_by_link_id(
            fake_links.safe_resp.link_id, current_user.user_id
        )
