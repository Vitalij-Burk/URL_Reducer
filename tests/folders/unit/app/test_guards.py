from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.folders.app.guards import FolderGuard
from src.folders.core.domain.exceptions.folder import FolderForbidden
from src.users.core.domain.schemas.inner.user import UserResponseInner


@pytest.mark.asyncio
async def test_check_user_ownership_by_folder_id_success(fake_users, fake_folders):
    current_user = fake_users.safe_resp
    mock_folder_manager = AsyncMock()
    guard = FolderGuard(mock_folder_manager)
    mock_folder_manager.get_by_id.return_value = fake_folders.inner_resp
    result = await guard.check_user_ownership_by_folder_id(
        fake_folders.safe_resp.folder_id, current_user.user_id
    )
    assert result is None


@pytest.mark.asyncio
async def test_check_user_ownership_by_folder_id_forbidden(fake_folders):
    current_user = UserResponseInner(
        user_id=uuid4(),
        name="fasfas",
        email="em@fad.con",
        hashed_password="fafdsafas",
        link_ids=[],
        folder_ids=[],
    )
    mock_folder_manager = AsyncMock()
    guard = FolderGuard(mock_folder_manager)
    mock_folder_manager.get_by_id.return_value = fake_folders.inner_resp
    with pytest.raises(FolderForbidden):
        await guard.check_user_ownership_by_folder_id(
            fake_folders.safe_resp.folder_id, current_user.user_id
        )
