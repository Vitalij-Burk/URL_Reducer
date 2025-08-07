from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.folders.infrastructure.storages.folder_repository_manager import (
    FolderRepositoryManager,
)
from src.links.app.decorators import check_user_ownership_by_folder_id
from src.links.app.decorators import check_user_ownership_by_link_id
from src.links.app.guards import LinkGuard
from src.links.core.domain.schemas.out.link import CreateLinkRequest
from src.links.core.domain.schemas.out.link import DeletedLinkResponse
from src.links.core.domain.schemas.out.link import LinkResponse
from src.links.core.domain.schemas.out.link import MoveLinkRequest
from src.links.core.domain.schemas.out.link import UpdateLinkRequest
from src.links.core.use_cases.link.create import CreateLinkUseCase
from src.links.core.use_cases.link.delete import DeleteLinkUseCase
from src.links.core.use_cases.link.get_by_id import GetLinkByIdUseCase
from src.links.core.use_cases.link.move import MoveLinkUseCase
from src.links.core.use_cases.link.update import UpdateLinkUseCase
from src.links.core.utils.random.string import get_random_string
from src.links.core.utils.serializers.link.from_inner import (
    serialize_to_safe_deleted_link,
)
from src.links.core.utils.serializers.link.from_inner import serialize_to_safe_link
from src.links.core.utils.serializers.link.from_safe import (
    serialize_to_create_inner_link,
)
from src.links.core.utils.serializers.link.from_safe import serialize_to_move_inner_link
from src.links.core.utils.serializers.link.from_safe import (
    serialize_to_update_inner_link,
)
from src.links.infrastructure.storages.link_repository_manager import (
    LinkRepositoryManager,
)


class LinkService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.link_manager = LinkRepositoryManager(db, client)
        self.folder_manager = FolderRepositoryManager(db, client)
        self.guard = LinkGuard(self.link_manager, self.folder_manager)
        self.create_link_use_case = CreateLinkUseCase(repo=self.link_manager)
        self.get_link_by_id_use_case = GetLinkByIdUseCase(repo=self.link_manager)
        self.update_link_use_case = UpdateLinkUseCase(repo=self.link_manager)
        self.move_link_use_case = MoveLinkUseCase(repo=self.link_manager)
        self.delete_link_use_case = DeleteLinkUseCase(repo=self.link_manager)

    async def create_link(
        self, body: CreateLinkRequest, current_user_id: UUID
    ) -> LinkResponse:
        link = serialize_to_create_inner_link(
            body, current_user_id, get_random_string()
        )
        return serialize_to_safe_link(await self.create_link_use_case.execute(link))

    @check_user_ownership_by_link_id
    async def get_link_by_id(
        self, link_id: UUID, current_user_id: UUID
    ) -> LinkResponse:
        return serialize_to_safe_link(
            await self.get_link_by_id_use_case.execute(link_id)
        )

    @check_user_ownership_by_link_id
    async def update_link(
        self, link_id: UUID, body: UpdateLinkRequest, current_user_id: UUID
    ) -> LinkResponse:
        return serialize_to_safe_link(
            await self.update_link_use_case.execute(
                link_id, serialize_to_update_inner_link(body)
            )
        )

    @check_user_ownership_by_link_id
    @check_user_ownership_by_folder_id
    async def move_link(
        self, link_id: UUID, body: MoveLinkRequest, current_user_id: UUID
    ) -> LinkResponse:
        return serialize_to_safe_link(
            await self.move_link_use_case.execute(
                link_id, serialize_to_move_inner_link(body)
            )
        )

    @check_user_ownership_by_link_id
    async def delete_link(
        self, link_id: UUID, current_user_id: UUID
    ) -> DeletedLinkResponse:
        return serialize_to_safe_deleted_link(
            await self.delete_link_use_case.execute(link_id)
        )
