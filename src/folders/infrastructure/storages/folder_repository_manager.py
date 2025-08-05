from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.exceptions.base import AppError
from src.core.domain.logger import app_logger
from src.folders.core.base_componenets.repositories.folder.db import IFolderRepository
from src.folders.core.domain.schemas.inner.folder import CreateFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import DeletedFolderResponseInner
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.inner.folder import MoveFolderRequestInner
from src.folders.core.domain.schemas.inner.folder import UpdateFolderRequestInner
from src.folders.infrastructure.storages.cache.unit_of_work import (
    UnitOfWork as CacheUnitOfWork,
)
from src.folders.infrastructure.storages.db.unit_of_work import (
    UnitOfWork as DBUnitOfWork,
)


class FolderRepositoryManager(IFolderRepository):
    def __init__(self, session: AsyncSession, client: Redis):
        self.db_uow = DBUnitOfWork(session)
        self.cache_uow = CacheUnitOfWork(client)

    async def create(self, entity: CreateFolderRequestInner) -> FolderResponseInner:
        async with self.db_uow as uow:
            return await uow.folders.create(entity)

    async def get_by_id(self, id: UUID) -> FolderResponseInner | None:
        folder = None
        try:
            folder = await self.cache_uow.folders.get_by_id(id)
        except AppError as err:
            app_logger.info(f"Cache access error: '{err}'")

        if folder is not None:
            return folder

        async with self.db_uow as uow:
            folder = await uow.folders.get_by_id(id)

        if folder is not None:
            try:
                await self.cache_uow.folders.cache_by_id(folder.folder_id, folder)
            except Exception as e:
                app_logger.error(f"Cache error: {e}")

        return folder

    async def update(
        self, id: UUID, update_folder_params: UpdateFolderRequestInner
    ) -> FolderResponseInner | None:
        async with self.db_uow as uow:
            folder = await uow.folders.update(id, update_folder_params)
        try:
            await self.cache_uow.folders.delete_by_id(folder.folder_id)
            await self.cache_uow.folders.cache_by_id(folder.folder_id, folder)
        finally:
            return folder

    async def move(
        self, id: UUID, move_folder_params: MoveFolderRequestInner
    ) -> FolderResponseInner | None:
        async with self.db_uow as uow:
            folder = await uow.folders.move(id, move_folder_params)
        try:
            await self.cache_uow.folders.delete_by_id(folder.folder_id)
            await self.cache_uow.folders.cache_by_id(folder.folder_id, folder)
        finally:
            return folder

    async def delete(self, id: UUID) -> DeletedFolderResponseInner | None:
        async with self.db_uow as uow:
            folder = await uow.folders.get_by_id(id)
        try:
            await self.cache_uow.folders.delete_by_id(folder.folder_id)
        finally:
            async with self.db_uow as uow:
                deleted_folder_response = await self.db_uow.folders.delete(id)
            return deleted_folder_response
