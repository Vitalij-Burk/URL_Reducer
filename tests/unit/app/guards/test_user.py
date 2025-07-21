from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.app.guards.user import UserGuard
from src.core.domain.exceptions.user import UserForbidden
from src.core.domain.schemas.dataclasses.user import UserResponseInner


@pytest.mark.asyncio
async def test_check_user_ownership_by_id_success(fake_users):
    current_user = fake_users.safe_resp
    mock_user_manager = AsyncMock()
    guard = UserGuard(mock_user_manager)
    mock_user_manager.get_by_id.return_value = fake_users.inner_resp
    result = await guard.check_user_ownership_by_id(
        fake_users.safe_resp.user_id, current_user
    )
    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_id_forbidden(fake_users):
    current_user = UserResponseInner(
        user_id=uuid4(),
        name="fasfas",
        email="em@fad.con",
        hashed_password="fafdsafas",
        links=[],
    )
    mock_user_manager = AsyncMock()
    guard = UserGuard(mock_user_manager)
    mock_user_manager.get_by_id.return_value = fake_users.inner_resp
    with pytest.raises(UserForbidden):
        await guard.check_user_ownership_by_id(
            fake_users.safe_resp.user_id, current_user
        )


@pytest.mark.asyncio
async def test_check_user_ownership_by_email_success(fake_users):
    current_user = fake_users.safe_resp
    mock_user_manager = AsyncMock()
    guard = UserGuard(mock_user_manager)
    mock_user_manager.get_by_id.return_value = fake_users.inner_resp
    result = await guard.check_user_ownership_by_email(
        fake_users.safe_resp.email, current_user
    )
    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_email_forbidden(fake_users):
    current_user = UserResponseInner(
        user_id=uuid4(),
        name="fasfas",
        email="em@fad.con",
        hashed_password="fafdsafas",
        links=[],
    )
    mock_user_manager = AsyncMock()
    guard = UserGuard(mock_user_manager)
    mock_user_manager.get_by_id.return_value = fake_users.inner_resp
    with pytest.raises(UserForbidden):
        await guard.check_user_ownership_by_email(
            fake_users.safe_resp.email, current_user
        )
