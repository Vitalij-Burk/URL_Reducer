from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.link import LinkService
from src.core.domain.schemas.general.link import UpdateLinkRequest
from src.core.domain.schemas.safe.link import CreateLink


@pytest.mark.asyncio
async def test_create_link_success(fake_users, fake_links):
    current_user = fake_users.safe
    mock_db = AsyncMock(spec=AsyncSession)
    mock_redis = AsyncMock(spec=Redis)
    service = LinkService(mock_db, mock_redis)

    service.link_manager = AsyncMock()
    service.link_manager.create.return_value = fake_links.inner

    create_link_payload = CreateLink(name="test", original_url="https://yt.com/")

    with patch(
        "src.app.services.link.get_random_string", return_value="fdsf12As"
    ) as mock_random_string, patch(
        "src.app.services.link.pydantic_create_link_to_inner",
        return_value=fake_links.inner,
    ) as mock_serializer, patch(
        "src.app.services.link.pydantic_inner_link_to_safe",
        return_value=fake_links.safe,
    ) as mock_to_safe:

        result = await service.create_link(
            create_link_payload, current_user=current_user
        )

        mock_random_string.assert_called_once()
        mock_serializer.assert_called_once()
        service.link_manager.create.assert_called_once()
        mock_to_safe.assert_called_once_with(fake_links.inner)

        assert str(result.original_url) == "https://yt.com/"


@pytest.mark.asyncio
async def test_get_link_by_id_success(fake_users, fake_links):
    current_user = fake_users.safe
    service = LinkService(db=AsyncMock(), client=AsyncMock())
    service.link_manager = AsyncMock()
    service.link_manager.get_by_id.return_value = fake_links.inner
    service.guard = AsyncMock()
    service.guard.check_user_ownership_by_link_id.return_value = None

    with patch(
        "src.app.services.link.pydantic_inner_link_to_safe",
        return_value=fake_links.safe,
    ):

        result = await service.get_link_by_id(
            link_id=fake_links.safe.link_id, current_user=current_user
        )

        service.link_manager.get_by_id.assert_called_once_with(fake_links.safe.link_id)
        assert result.link_id == fake_links.safe.link_id


@pytest.mark.asyncio
async def test_update_link_success(fake_users, fake_links):
    current_user = fake_users.safe
    service = LinkService(db=AsyncMock(), client=AsyncMock())
    service.link_manager = AsyncMock()
    service.link_manager.update.return_value = fake_links.inner
    update_link_params = UpdateLinkRequest(name="updated_test")
    service.guard = AsyncMock()
    service.guard.check_user_ownership_by_link_id.return_value = None

    with patch(
        "src.app.services.link.pydantic_inner_link_to_safe",
        return_value=fake_links.safe,
    ):

        result = await service.update_link(
            link_id=fake_links.safe.link_id,
            body=update_link_params,
            current_user=current_user,
        )

        service.link_manager.update.assert_called_once_with(
            fake_links.safe.link_id, update_link_params.model_dump()
        )
        assert result.link_id == fake_links.safe.link_id


@pytest.mark.asyncio
async def test_delete_link_success(fake_users, fake_links):
    current_user = fake_users.safe
    service = LinkService(db=AsyncMock(), client=AsyncMock())
    service.link_manager = AsyncMock()
    service.link_manager.delete.return_value = fake_links.inner
    service.guard = AsyncMock()
    service.guard.check_user_ownership_by_link_id.return_value = None

    with patch(
        "src.app.services.link.pydantic_inner_link_to_safe",
        return_value=fake_links.safe,
    ):

        result = await service.delete_link(
            link_id=fake_links.safe.link_id, current_user=current_user
        )

        service.link_manager.delete.assert_called_once_with(fake_links.safe.link_id)
        assert result.link_id == fake_links.safe.link_id
