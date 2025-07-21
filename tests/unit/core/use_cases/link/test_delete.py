from unittest.mock import AsyncMock

import pytest

from src.core.use_cases.link.delete import DeleteLinkUseCase


@pytest.mark.asyncio
async def test_delete_link_use_case(fake_links):
    repo = AsyncMock()
    delete_link_use_case = DeleteLinkUseCase(repo)

    repo.delete.return_value = fake_links.inner_del

    result = await delete_link_use_case.execute(fake_links.inner_resp.link_id)

    repo.delete.assert_awaited_once_with(fake_links.inner_resp.link_id)
    assert result == fake_links.inner_del
