from unittest.mock import AsyncMock

import pytest

from src.links.core.use_cases.link.create import CreateLinkUseCase


@pytest.mark.asyncio
async def test_create_link_use_case(fake_links):
    repo = AsyncMock()
    create_link_use_case = CreateLinkUseCase(repo)

    repo.create.return_value = fake_links.inner_resp

    result = await create_link_use_case.execute(fake_links.inner_create)

    repo.create.assert_awaited_once_with(fake_links.inner_create)
    assert result == fake_links.inner_resp
