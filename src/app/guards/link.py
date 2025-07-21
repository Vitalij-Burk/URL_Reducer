from uuid import UUID

from src.core.domain.exceptions.link import LinkForbidden
from src.core.domain.exceptions.link import LinkNotFound
from src.core.domain.schemas.pydantic.user import UserResponse
from src.infrastructure.storages.manager.link_repository_manager import (
    LinkRepositoryManager,
)


class LinkGuard:
    def __init__(self, link_manager: LinkRepositoryManager):
        self.link_manager = link_manager

    async def check_user_ownership_by_link_id(
        self, link_id: UUID, current_user: UserResponse
    ):
        link = await self.link_manager.get_by_id(link_id)
        if link.user_id != current_user.user_id:
            raise LinkForbidden(link.user_id, current_user.user_id)
