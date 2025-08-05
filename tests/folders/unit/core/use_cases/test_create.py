from unittest.mock import AsyncMock

import pytest

from src.folders.core.use_cases.folder.create import CreateFolderUseCase


@pytest.mark.asyncio
async def test_create_folder_use_case(fake_folders):
    repo = AsyncMock()
    create_folder_use_case = CreateFolderUseCase(repo)

    repo.create.return_value = fake_folders.inner_resp

    result = await create_folder_use_case.execute(fake_folders.inner_create)

    repo.create.assert_awaited_once_with(fake_folders.inner_create)
    assert result == fake_folders.inner_resp
