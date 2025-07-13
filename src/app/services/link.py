from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.decorators.link import check_user_ownership_by_link_id
from src.app.guards.link import LinkGuard
from src.app.utils.random import get_random_string
from src.core.domain.schemas.general.link import DeletedLinkResponse
from src.core.domain.schemas.general.link import UpdateLinkRequest
from src.core.domain.schemas.safe.link import CreateLink
from src.core.domain.schemas.safe.link import LinkResponse
from src.core.domain.schemas.safe.user import UserResponse
from src.core.utils.serializers.from_pydantic.link import pydantic_create_link_to_inner
from src.core.utils.serializers.from_pydantic.link import pydantic_inner_link_to_safe
from src.infrastructure.storages.manager.link_repository_manager import (
    LinkRepositoryManager,
)


class LinkService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.link_manager = LinkRepositoryManager(db, client)
        self.guard = LinkGuard(self.link_manager)

    async def create_link(
        self, body: CreateLink, current_user: UserResponse
    ) -> LinkResponse:
        link = await self.link_manager.create(
            pydantic_create_link_to_inner(
                body, current_user.user_id, get_random_string()
            )
        )
        return pydantic_inner_link_to_safe(link)

    @check_user_ownership_by_link_id
    async def get_link_by_id(
        self, link_id: UUID, current_user: UserResponse
    ) -> LinkResponse:
        link = await self.link_manager.get_by_id(link_id)
        return pydantic_inner_link_to_safe(link)

    @check_user_ownership_by_link_id
    async def update_link(
        self, link_id: UUID, body: UpdateLinkRequest, current_user: UserResponse
    ) -> LinkResponse:
        updated_link = await self.link_manager.update(link_id, body.model_dump())
        return pydantic_inner_link_to_safe(updated_link)

    @check_user_ownership_by_link_id
    async def delete_link(
        self, link_id: UUID, current_user: UserResponse
    ) -> DeletedLinkResponse:
        deleted_link_resp = await self.link_manager.delete(link_id)
        return deleted_link_resp
