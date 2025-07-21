from unittest.mock import AsyncMock

import pytest

from src.core.domain.exceptions.link import LinkLimitExceeded
from src.core.domain.schemas.dataclasses.link import UpdateLinkRequestInner
from src.core.use_cases.redirect.redirect import RedirectUseCase


@pytest.mark.asyncio
async def test_redirect_use_case_success(fake_links):
    repo = AsyncMock()
    redirect_use_case = RedirectUseCase(repo)
    repo.get_by_short_code.return_value = fake_links.inner_resp
    repo.update.return_value = fake_links.inner_resp

    result = await redirect_use_case.execute("fadFsd12")

    repo.get_by_short_code.assert_awaited_once_with("fadFsd12")
    repo.update.assert_awaited_once_with(
        fake_links.inner_resp.link_id,
        UpdateLinkRequestInner(clicks=fake_links.inner_resp.clicks + 1),
    )
    assert result == fake_links.inner_resp.original_url


@pytest.mark.asyncio
async def test_redirect_use_case_limit_exceeded(fake_links):
    repo = AsyncMock()
    redirect_use_case = RedirectUseCase(repo)
    fake_links.inner_resp.clicks = 10
    repo.get_by_short_code.return_value = fake_links.inner_resp
    repo.update.return_value = fake_links.inner_resp

    with pytest.raises(LinkLimitExceeded):
        await redirect_use_case.execute("fadFsd12")
