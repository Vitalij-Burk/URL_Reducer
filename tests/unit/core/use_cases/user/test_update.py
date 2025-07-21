from unittest.mock import AsyncMock

import pytest

from src.core.domain.schemas.dataclasses.user import UpdateUserRequestInner
from src.core.use_cases.user.update import UpdateUserUseCase


@pytest.mark.asyncio
async def test_update_user_use_case(fake_users):
    repo = AsyncMock()
    update_user_use_case = UpdateUserUseCase(repo)

    repo.update.return_value = fake_users.inner_resp

    result = await update_user_use_case.execute(
        fake_users.inner_resp.user_id, UpdateUserRequestInner(name="fadfasf")
    )

    repo.update.assert_awaited_once_with(
        fake_users.inner_resp.user_id, UpdateUserRequestInner(name="fadfasf")
    )
    assert result == fake_users.inner_resp
