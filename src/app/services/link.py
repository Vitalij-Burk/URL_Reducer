from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.decorators.link import check_user_ownership_by_link_id
from src.app.guards.link import LinkGuard
from src.core.domain.schemas.pydantic.link import CreateLink
from src.core.domain.schemas.pydantic.link import DeletedLinkResponse
from src.core.domain.schemas.pydantic.link import LinkResponse
from src.core.domain.schemas.pydantic.link import UpdateLinkRequest
from src.core.domain.schemas.pydantic.user import UserResponse
from src.core.use_cases.link.create import CreateLinkUseCase
from src.core.use_cases.link.delete import DeleteLinkUseCase
from src.core.use_cases.link.get_by_id import GetLinkByIdUseCase
from src.core.use_cases.link.update import UpdateLinkUseCase
from src.core.utils.random.string import get_random_string
from src.core.utils.serializers.from_inner.link import serialize_to_safe_deleted_link
from src.core.utils.serializers.from_inner.link import serialize_to_safe_link
from src.core.utils.serializers.from_safe.link import serialize_to_create_inner_link
from src.core.utils.serializers.from_safe.link import serialize_to_update_inner_link
from src.infrastructure.storages.manager.link_repository_manager import (
    LinkRepositoryManager,
)


class LinkService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.link_manager = LinkRepositoryManager(db, client)
        self.guard = LinkGuard(self.link_manager)
        self.create_link_use_case = CreateLinkUseCase(repo=self.link_manager)
        self.get_link_by_id_use_case = GetLinkByIdUseCase(repo=self.link_manager)
        self.update_link_use_case = UpdateLinkUseCase(repo=self.link_manager)
        self.delete_link_use_case = DeleteLinkUseCase(repo=self.link_manager)

    async def create_link(
        self, body: CreateLink, current_user: UserResponse
    ) -> LinkResponse:
        link = serialize_to_create_inner_link(
            body, current_user.user_id, get_random_string()
        )
        return serialize_to_safe_link(await self.create_link_use_case.execute(link))

    @check_user_ownership_by_link_id
    async def get_link_by_id(
        self, link_id: UUID, current_user: UserResponse
    ) -> LinkResponse:
        return serialize_to_safe_link(
            await self.get_link_by_id_use_case.execute(link_id)
        )

    @check_user_ownership_by_link_id
    async def update_link(
        self, link_id: UUID, body: UpdateLinkRequest, current_user: UserResponse
    ) -> LinkResponse:
        return serialize_to_safe_link(
            await self.update_link_use_case.execute(
                link_id, serialize_to_update_inner_link(body)
            )
        )

    @check_user_ownership_by_link_id
    async def delete_link(
        self, link_id: UUID, current_user: UserResponse
    ) -> DeletedLinkResponse:
        return serialize_to_safe_deleted_link(
            await self.delete_link_use_case.execute(link_id)
        )
