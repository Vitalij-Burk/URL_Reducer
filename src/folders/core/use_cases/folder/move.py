from uuid import UUID

from src.folders.core.base_componenets.repositories.db import IFolderRepository
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.inner.folder import MoveFolderRequestInner


class MoveFolderUseCase:
    def __init__(self, repo: IFolderRepository):
        self.repo = repo

    async def execute(
        self, folder_id: UUID, update_folder_params: MoveFolderRequestInner
    ) -> FolderResponseInner:
        moved_folder = await self.repo.move(folder_id, update_folder_params)
        return moved_folder
