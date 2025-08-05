from unittest.mock import AsyncMock

import pytest

from src.links.core.domain.schemas.inner.link import MoveLinkRequestInner
from src.links.core.use_cases.link.move import MoveLinkUseCase


@pytest.mark.asyncio
async def test_move_link_use_case(fake_links):
    repo = AsyncMock()
    move_link_use_case = MoveLinkUseCase(repo)

    repo.move.return_value = fake_links.inner_resp

    result = await move_link_use_case.execute(
        fake_links.inner_resp.link_id, MoveLinkRequestInner(folder_id=None)
    )

    repo.move.assert_awaited_once_with(
        fake_links.inner_resp.link_id, MoveLinkRequestInner(folder_id=None)
    )
    assert result == fake_links.inner_resp
