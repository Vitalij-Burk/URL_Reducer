from unittest.mock import AsyncMock
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from src.app.services.redirect import RedirectService
from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.domain.schemas.safe.link import LinkResponse


@pytest.mark.asyncio
async def test_redirect_success(fake_links):
    service = RedirectService(db=AsyncMock(), client=AsyncMock())
    service.link_manager.get_by_short_code = AsyncMock(return_value=fake_links.inner)
    service.link_manager.update = AsyncMock(return_value=fake_links.inner)

    with patch(
        "src.app.services.redirect.pydantic_inner_link_to_safe",
        return_value=fake_links.safe,
    ):
        result = await service.redirect(fake_links.safe.short_code)

    assert isinstance(result, RedirectResponse)


@pytest.mark.asyncio
async def test_redirect_limit_exceeded():
    link_id = uuid4()
    user_id = uuid4()
    fake_safe = LinkResponse(
        link_id=link_id,
        user_id=user_id,
        name="test",
        original_url="https://yt.com",
        short_url="http://localhost:8000/f12Qsds3",
        short_code="f12Qsds3",
        clicks=11,
    )
    fake_inner = LinkResponseInner(
        link_id=link_id,
        user_id=user_id,
        name="test",
        original_url="https://yt.com",
        short_code="f12Qsds3",
        clicks=11,
    )
    service = RedirectService(db=AsyncMock(), client=AsyncMock())
    service.link_manager.get_by_short_code = AsyncMock(return_value=fake_inner)

    with pytest.raises(HTTPException) as exc:
        await service.redirect(fake_safe.short_code)

    assert exc.value.status_code == 406
    assert exc.value.detail == "Limit of link uses exceeded."


@pytest.mark.asyncio
async def test_redirect_not_found(fake_links):
    service = RedirectService(db=AsyncMock(), client=AsyncMock())
    service.link_manager.get_by_short_code = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc:
        await service.redirect(fake_links.safe.short_code)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Original URL link not found."
