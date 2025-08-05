from unittest.mock import AsyncMock

import pytest

from src.links.core.use_cases.link.get_by_id import GetLinkByIdUseCase


@pytest.mark.asyncio
async def test_get_link_by_id_use_case(fake_links):
    repo = AsyncMock()
    get_link_by_id_use_case = GetLinkByIdUseCase(repo)

    repo.get_by_id.return_value = fake_links.inner_resp

    result = await get_link_by_id_use_case.execute(fake_links.inner_resp.link_id)

    repo.get_by_id.assert_awaited_once_with(fake_links.inner_resp.link_id)
    assert result == fake_links.inner_resp
