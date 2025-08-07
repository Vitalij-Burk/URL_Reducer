from uuid import UUID

from src.folders.core.domain.exceptions.folder import FolderForbidden
from src.folders.infrastructure.storages.folder_repository_manager import (
    FolderRepositoryManager,
)


class FolderGuard:
    def __init__(self, folder_manager: FolderRepositoryManager):
        self.folder_manager = folder_manager

    async def check_user_ownership_by_folder_id(
        self, folder_id: UUID, current_user_id: UUID
    ):
        folder = await self.folder_manager.get_by_id(folder_id)
        if folder.user_id != current_user_id:
            raise FolderForbidden(current_user_id, folder.folder_id)
