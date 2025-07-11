from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.app.guards.user import UserGuard
from src.core.domain.http_errors import ForbiddenError


@pytest.mark.asyncio
async def test_check_user_ownership_by_id_success(fake_users):
    current_user = fake_users.safe
    user_id = current_user.user_id
    guard = UserGuard(AsyncMock())

    result = await guard.check_user_ownership_by_id(user_id, current_user)

    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_id_forbidden(fake_users):
    current_user = fake_users.safe
    user_id = uuid4()
    guard = UserGuard(AsyncMock())

    with pytest.raises(ForbiddenError):
        await guard.check_user_ownership_by_id(user_id, current_user)


@pytest.mark.asyncio
async def test_check_user_ownership_by_email_success(fake_users):
    current_user = fake_users.safe
    email = current_user.email
    guard = UserGuard(AsyncMock())

    result = await guard.check_user_ownership_by_email(email, current_user)

    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_email_forbidden(fake_users):
    current_user = fake_users.safe
    user_id = "user@mail.com"
    guard = UserGuard(AsyncMock())

    with pytest.raises(ForbiddenError):
        await guard.check_user_ownership_by_email(user_id, current_user)
