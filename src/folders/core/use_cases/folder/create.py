from src.folders.core.base_componenets.repositories.folder.db import IFolderRepository
from src.folders.core.domain.schemas.inner.folder import CreateFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner


class CreateFolderUseCase:
    def __init__(self, repo: IFolderRepository):
        self.repo = repo

    async def execute(self, dto: CreateFolderRequestInner) -> FolderResponseInner:
        folder = await self.repo.create(dto)
        return folder
