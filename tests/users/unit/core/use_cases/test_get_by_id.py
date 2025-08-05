from unittest.mock import AsyncMock

import pytest

from src.users.core.use_cases.user.get_by_id import GetUserByIdUseCase


@pytest.mark.asyncio
async def test_get_user_by_id_use_case(fake_users):
    repo = AsyncMock()
    get_user_by_id_use_case = GetUserByIdUseCase(repo)

    repo.get_by_id.return_value = fake_users.inner_resp

    result = await get_user_by_id_use_case.execute(fake_users.inner_resp.user_id)

    repo.get_by_id.assert_awaited_once_with(fake_users.inner_resp.user_id)
    assert result == fake_users.inner_resp
