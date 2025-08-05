from unittest.mock import AsyncMock

import pytest

from src.folders.core.domain.schemas.inner.folder import MoveFolderRequestInner
from src.folders.core.use_cases.folder.move import MoveFolderUseCase


@pytest.mark.asyncio
async def test_move_folder_use_case(fake_folders):
    repo = AsyncMock()
    move_folder_use_case = MoveFolderUseCase(repo)

    repo.move.return_value = fake_folders.inner_resp

    result = await move_folder_use_case.execute(
        fake_folders.inner_resp.folder_id, MoveFolderRequestInner(parent_id=None)
    )

    repo.move.assert_awaited_once_with(
        fake_folders.inner_resp.folder_id, MoveFolderRequestInner(parent_id=None)
    )
    assert result == fake_folders.inner_resp
