from sqlalchemy.ext.asyncio import AsyncSession

from src.folders.core.interfaces.repositories.units_of_work.db import IUnitOfWork
from src.folders.infrastructure.storages.db.repositories.folder import FolderRepository


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.folders = FolderRepository(session)

    async def flush(self):
        await self.session.flush()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
