from uuid import UUID

from src.folders.core.base_componenets.repositories.db import IFolderRepository
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.inner.folder import UpdateFolderRequestInner


class UpdateFolderUseCase:
    def __init__(self, repo: IFolderRepository):
        self.repo = repo

    async def execute(
        self, folder_id: UUID, update_folder_params: UpdateFolderRequestInner
    ) -> FolderResponseInner:
        updated_folder = await self.repo.update(folder_id, update_folder_params)
        return updated_folder
