from unittest.mock import AsyncMock

import pytest

from src.folders.core.use_cases.folder.get_by_id import GetFolderByIdUseCase


@pytest.mark.asyncio
async def test_get_folder_by_id_use_case(fake_folders):
    repo = AsyncMock()
    get_folder_by_id_use_case = GetFolderByIdUseCase(repo)

    repo.get_by_id.return_value = fake_folders.inner_resp

    result = await get_folder_by_id_use_case.execute(fake_folders.inner_resp.folder_id)

    repo.get_by_id.assert_awaited_once_with(fake_folders.inner_resp.folder_id)
    assert result == fake_folders.inner_resp
