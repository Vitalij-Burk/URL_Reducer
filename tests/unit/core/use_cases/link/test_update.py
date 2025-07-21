from unittest.mock import AsyncMock

import pytest

from src.core.domain.schemas.dataclasses.link import UpdateLinkRequestInner
from src.core.use_cases.link.update import UpdateLinkUseCase


@pytest.mark.asyncio
async def test_update_link_use_case(fake_links):
    repo = AsyncMock()
    update_link_use_case = UpdateLinkUseCase(repo)

    repo.update.return_value = fake_links.inner_resp

    result = await update_link_use_case.execute(
        fake_links.inner_resp.link_id, UpdateLinkRequestInner(name="fadfasf")
    )

    repo.update.assert_awaited_once_with(
        fake_links.inner_resp.link_id, UpdateLinkRequestInner(name="fadfasf")
    )
    assert result == fake_links.inner_resp
