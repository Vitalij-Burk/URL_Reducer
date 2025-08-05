from dataclasses import asdict
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.logger import app_logger
from src.core.utils.serializers.to_dict import serialize_to_dict_exclude_none
from src.folders.core.base_componenets.repositories.folder.db import IFolderRepository
from src.folders.core.domain.exceptions.folder import FolderAlreadyExists
from src.folders.core.domain.exceptions.folder import FolderNotFound
from src.folders.core.domain.schemas.inner.folder import CreateFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import DeletedFolderResponseInner
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.inner.folder import MoveFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import UpdateFolderRequestInner
from src.folders.core.utils.serializers.folder.from_orm import serialize_to_inner_folder
from src.folders.infrastructure.storages.db.base.DAL.folder import FolderDAL


class FolderRepository(IFolderRepository):
    def __init__(self, session: AsyncSession):
        self.folder_dal = FolderDAL(session)

    async def create(self, entity: CreateFolderRequestInner) -> FolderResponseInner:
        try:
            new_folder = await self.folder_dal.create(**asdict(entity))
            return serialize_to_inner_folder(new_folder, include_inner_fields=False)
        except IntegrityError as err:
            app_logger.error(err)
            raise FolderAlreadyExists(str(entity))

    async def get_by_id(self, id: UUID) -> FolderResponseInner | None:
        folder = await self.folder_dal.get_by_id(id)
        if not folder:
            raise FolderNotFound(id)
        return serialize_to_inner_folder(folder)

    async def update(
        self, id: UUID, update_folder_params: UpdateFolderRequestInner
    ) -> FolderResponseInner | None:
        folder = await self.folder_dal.update(
            id,
            **serialize_to_dict_exclude_none(update_folder_params),
        )
        if not folder:
            raise FolderNotFound(id)
        return serialize_to_inner_folder(folder)

    async def move(
        self, id: UUID, move_folder_params: MoveFolderRequestInner
    ) -> FolderResponseInner | None:
        folder = await self.folder_dal.update(
            id,
            **asdict(move_folder_params),
        )
        if not folder:
            raise FolderNotFound(id)
        return serialize_to_inner_folder(folder)

    async def delete(self, id: UUID) -> DeletedFolderResponseInner | None:
        deleted_folder_id = await self.folder_dal.delete(id)
        return DeletedFolderResponseInner(deleted_folder_id=deleted_folder_id)
