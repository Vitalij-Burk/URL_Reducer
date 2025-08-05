from unittest.mock import AsyncMock

import pytest

from src.folders.core.domain.schemas.inner.folder import UpdateFolderRequestInner
from src.folders.core.use_cases.folder.update import UpdateFolderUseCase


@pytest.mark.asyncio
async def test_update_folder_use_case(fake_folders):
    repo = AsyncMock()
    update_folder_use_case = UpdateFolderUseCase(repo)

    repo.update.return_value = fake_folders.inner_resp

    result = await update_folder_use_case.execute(
        fake_folders.inner_resp.folder_id, UpdateFolderRequestInner(name="fadfasf")
    )

    repo.update.assert_awaited_once_with(
        fake_folders.inner_resp.folder_id, UpdateFolderRequestInner(name="fadfasf")
    )
    assert result == fake_folders.inner_resp
