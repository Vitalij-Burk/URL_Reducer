from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.folders.infrastructure.storages.db.base.models import Folder


class FolderDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, parent_id: UUID, name: str) -> Folder:
        new_folder = Folder(
            user_id=user_id,
            parent_id=parent_id,
            name=name,
        )
        self.session.add(new_folder)
        await self.session.flush()
        return new_folder

    async def get_by_id(self, folder_id: UUID) -> Folder | None:
        stmt = select(Folder).where(Folder.folder_id == folder_id)
        res = await self.session.execute(
            stmt.options(
                selectinload(Folder.links),
                selectinload(Folder.children),
            )
        )
        return res.scalar_one_or_none()

    async def update(self, folder_id: UUID, **kwargs) -> Folder | None:
        stmt = update(Folder).where(Folder.folder_id == folder_id).values(**kwargs)
        res = await self.session.execute(
            stmt.returning(Folder).options(
                selectinload(Folder.links),
                selectinload(Folder.children),
            )
        )
        return res.scalar_one_or_none()

    async def delete(self, folder_id: UUID) -> UUID | None:
        stmt = delete(Folder).where(Folder.folder_id == folder_id)
        res = await self.session.execute(stmt.returning(Folder.folder_id))
        return res.scalar_one_or_none()
