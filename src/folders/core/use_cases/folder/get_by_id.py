from uuid import UUID

from src.folders.core.base_componenets.repositories.db import IFolderRepository
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner


class GetFolderByIdUseCase:
    def __init__(self, repo: IFolderRepository):
        self.repo = repo

    async def execute(self, folder_id: UUID) -> FolderResponseInner:
        folder = await self.repo.get_by_id(folder_id)
        return folder
