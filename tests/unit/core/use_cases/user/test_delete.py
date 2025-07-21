from unittest.mock import AsyncMock

import pytest

from src.core.use_cases.user.delete import DeleteUserUseCase


@pytest.mark.asyncio
async def test_delete_user_use_case(fake_users):
    repo = AsyncMock()
    delete_user_use_case = DeleteUserUseCase(repo)

    repo.delete.return_value = fake_users.inner_del

    result = await delete_user_use_case.execute(fake_users.inner_resp.user_id)

    repo.delete.assert_awaited_once_with(fake_users.inner_resp.user_id)
    assert result == fake_users.inner_del
