from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.users.app.guards import UserGuard
from src.users.core.domain.exceptions.user import UserForbidden
from src.users.core.domain.schemas.inner.user import UserResponseInner


@pytest.mark.asyncio
async def test_check_user_ownership_by_id_success(fake_users):
    current_user = fake_users.safe_resp
    mock_user_manager = AsyncMock()
    guard = UserGuard(mock_user_manager)
    mock_user_manager.get_by_id.return_value = fake_users.inner_resp
    result = await guard.check_user_ownership_by_id(
        fake_users.safe_resp.user_id, current_user.user_id
    )
    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_id_forbidden(fake_users):
    current_user = UserResponseInner(
        user_id=uuid4(),
        name="fasfas",
        email="em@fad.con",
        hashed_password="fafdsafas",
        link_ids=[],
        folder_ids=[],
    )
    mock_user_manager = AsyncMock()
    guard = UserGuard(mock_user_manager)
    mock_user_manager.get_by_id.return_value = fake_users.inner_resp
    with pytest.raises(UserForbidden):
        await guard.check_user_ownership_by_id(
            fake_users.safe_resp.user_id, current_user.user_id
        )


@pytest.mark.asyncio
async def test_check_user_ownership_by_email_success(fake_users):
    current_user = fake_users.safe_resp
    mock_user_manager = AsyncMock()
    guard = UserGuard(mock_user_manager)
    mock_user_manager.get_by_id.return_value = fake_users.inner_resp
    result = await guard.check_user_ownership_by_email(
        fake_users.safe_resp.email, current_user.email
    )
    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_email_forbidden(fake_users):
    current_user = UserResponseInner(
        user_id=uuid4(),
        name="fasfas",
        email="em@fad.con",
        hashed_password="fafdsafas",
        link_ids=[],
        folder_ids=[],
    )
    mock_user_manager = AsyncMock()
    guard = UserGuard(mock_user_manager)
    mock_user_manager.get_by_id.return_value = fake_users.inner_resp
    with pytest.raises(UserForbidden):
        await guard.check_user_ownership_by_email(
            fake_users.safe_resp.email, current_user.email
        )
