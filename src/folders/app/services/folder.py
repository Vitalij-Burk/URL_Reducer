from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.folders.app.decorators import check_is_not_parent_folder
from src.folders.app.decorators import check_user_ownership_by_folder_id
from src.folders.app.decorators import check_user_ownership_by_move_id
from src.folders.app.guards import FolderGuard
from src.folders.core.domain.schemas.out.folder import CreateFolderRequest
from src.folders.core.domain.schemas.out.folder import DeletedFolderResponse
from src.folders.core.domain.schemas.out.folder import FolderResponse
from src.folders.core.domain.schemas.out.folder import MoveFolderRequest
from src.folders.core.domain.schemas.out.folder import UpdateFolderRequest
from src.folders.core.use_cases.folder.create import CreateFolderUseCase
from src.folders.core.use_cases.folder.delete import DeleteFolderUseCase
from src.folders.core.use_cases.folder.get_by_id import GetFolderByIdUseCase
from src.folders.core.use_cases.folder.move import MoveFolderUseCase
from src.folders.core.use_cases.folder.update import UpdateFolderUseCase
from src.folders.core.utils.serializers.folder.from_inner import (
    serialize_to_safe_deleted_folder,
)
from src.folders.core.utils.serializers.folder.from_inner import (
    serialize_to_safe_folder,
)
from src.folders.core.utils.serializers.folder.from_safe import (
    serialize_to_create_inner_folder,
)
from src.folders.core.utils.serializers.folder.from_safe import (
    serialize_to_move_inner_folder,
)
from src.folders.core.utils.serializers.folder.from_safe import (
    serialize_to_update_inner_folder,
)
from src.folders.infrastructure.storages.folder_repository_manager import (
    FolderRepositoryManager,
)


class FolderService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.folder_manager = FolderRepositoryManager(db, client)
        self.guard = FolderGuard(self.folder_manager)
        self.create_folder_use_case = CreateFolderUseCase(repo=self.folder_manager)
        self.get_folder_by_id_use_case = GetFolderByIdUseCase(repo=self.folder_manager)
        self.update_folder_use_case = UpdateFolderUseCase(repo=self.folder_manager)
        self.move_folder_use_case = MoveFolderUseCase(repo=self.folder_manager)
        self.delete_folder_use_case = DeleteFolderUseCase(repo=self.folder_manager)

    async def create_folder(
        self, body: CreateFolderRequest, current_user_id: UUID
    ) -> FolderResponse:
        folder = serialize_to_create_inner_folder(body, current_user_id)
        return serialize_to_safe_folder(
            await self.create_folder_use_case.execute(folder),
            include_inner_fields=False,
        )

    @check_user_ownership_by_folder_id
    async def get_folder_by_id(
        self, folder_id: UUID, current_user_id: UUID
    ) -> FolderResponse:
        return serialize_to_safe_folder(
            await self.get_folder_by_id_use_case.execute(folder_id)
        )

    @check_user_ownership_by_folder_id
    async def update_folder(
        self, folder_id: UUID, body: UpdateFolderRequest, current_user_id: UUID
    ) -> FolderResponse:
        return serialize_to_safe_folder(
            await self.update_folder_use_case.execute(
                folder_id, serialize_to_update_inner_folder(body)
            )
        )

    @check_user_ownership_by_folder_id
    @check_user_ownership_by_move_id
    @check_is_not_parent_folder
    async def move_folder(
        self, folder_id: UUID, body: MoveFolderRequest, current_user_id: UUID
    ) -> FolderResponse:
        return serialize_to_safe_folder(
            await self.move_folder_use_case.execute(
                folder_id, serialize_to_move_inner_folder(body)
            )
        )

    @check_user_ownership_by_folder_id
    async def delete_folder(
        self, folder_id: UUID, current_user_id: UUID
    ) -> DeletedFolderResponse:
        return serialize_to_safe_deleted_folder(
            await self.delete_folder_use_case.execute(folder_id)
        )
