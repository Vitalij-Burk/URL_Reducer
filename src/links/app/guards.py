from uuid import UUID

from src.folders.core.domain.exceptions.folder import FolderForbidden
from src.folders.infrastructure.storages.folder_repository_manager import (
    FolderRepositoryManager,
)
from src.links.core.domain.exceptions.link import LinkForbidden
from src.links.infrastructure.storages.link_repository_manager import (
    LinkRepositoryManager,
)


class LinkGuard:
    def __init__(
        self,
        link_manager: LinkRepositoryManager,
        folder_manager: FolderRepositoryManager,
    ):
        self.link_manager = link_manager
        self.folder_manager = folder_manager

    async def check_user_ownership_by_link_id(
        self, link_id: UUID, current_user_id: UUID
    ):
        link = await self.link_manager.get_by_id(link_id)
        if link.user_id != current_user_id:
            raise LinkForbidden(link.user_id, current_user_id)

    async def check_user_ownership_by_folder_id(
        self, folder_id: UUID, current_user_id: UUID
    ):
        folder = await self.folder_manager.get_by_id(folder_id)
        if folder.user_id != current_user_id:
            raise FolderForbidden(current_user_id, folder.folder_id)
