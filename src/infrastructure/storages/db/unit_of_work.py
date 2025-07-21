from sqlalchemy.ext.asyncio import AsyncSession

from src.core.interfaces.repositories.units_of_work.db import IUnitOfWork
from src.infrastructure.storages.db.repositories.link import LinkRepository
from src.infrastructure.storages.db.repositories.user import UserRepository


class UnitOfWork(IUnitOfWork):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)
        self.links = LinkRepository(session)

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
