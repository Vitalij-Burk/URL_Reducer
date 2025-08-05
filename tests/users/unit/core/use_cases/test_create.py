from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest

from src.users.core.use_cases.user.create import CreateUserUseCase


@pytest.mark.asyncio
async def test_create_user_use_case(fake_users):
    repo = AsyncMock()
    hasher = Mock()
    create_user_use_case = CreateUserUseCase(repo, hasher)

    repo.create.return_value = fake_users.inner_resp

    result = await create_user_use_case.execute(fake_users.inner_create)

    repo.create.assert_awaited_once_with(fake_users.inner_create)
    assert result == fake_users.inner_resp
