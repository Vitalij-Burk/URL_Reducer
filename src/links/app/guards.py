from uuid import UUID

from src.links.core.domain.exceptions.link import LinkForbidden
from src.links.infrastructure.storages.link_repository_manager import (
    LinkRepositoryManager,
)


class LinkGuard:
    def __init__(self, link_manager: LinkRepositoryManager):
        self.link_manager = link_manager

    async def check_user_ownership_by_link_id(
        self, link_id: UUID, current_user_id: UUID
    ):
        link = await self.link_manager.get_by_id(link_id)
        if link.user_id != current_user_id:
            raise LinkForbidden(link.user_id, current_user_id)
