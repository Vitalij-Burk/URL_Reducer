from unittest.mock import AsyncMock

import pytest

from src.folders.core.use_cases.folder.delete import DeleteFolderUseCase


@pytest.mark.asyncio
async def test_delete_folder_use_case(fake_folders):
    repo = AsyncMock()
    delete_folder_use_case = DeleteFolderUseCase(repo)

    repo.delete.return_value = fake_folders.inner_del

    result = await delete_folder_use_case.execute(fake_folders.inner_resp.folder_id)

    repo.delete.assert_awaited_once_with(fake_folders.inner_resp.folder_id)
    assert result == fake_folders.inner_del
