from uuid import UUID

from src.folders.core.base_componenets.repositories.folder.db import IFolderRepository
from src.folders.core.domain.schemas.inner.folder import DeletedFolderResponseInner


class DeleteFolderUseCase:
    def __init__(self, repo: IFolderRepository):
        self.repo = repo

    async def execute(self, folder_id: UUID) -> DeletedFolderResponseInner:
        resp = await self.repo.delete(folder_id)
        return resp
