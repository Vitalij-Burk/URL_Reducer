from unittest.mock import AsyncMock

import pytest

from src.core.use_cases.user.get_by_email import GetUserByEmailUseCase


@pytest.mark.asyncio
async def test_get_user_by_email_use_case_success(fake_users):
    repo = AsyncMock()
    get_user_by_email_use_case = GetUserByEmailUseCase(repo)

    repo.get_by_email.return_value = fake_users.inner_resp

    result = await get_user_by_email_use_case.execute(fake_users.inner_resp.email)

    repo.get_by_email.assert_awaited_once_with(fake_users.inner_resp.email)
    assert result == fake_users.inner_resp
