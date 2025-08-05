from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.links.infrastructure.storages.db.base.models import Link


class LinkDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: UUID,
        name: str,
        original_url: str,
        short_code: str,
        folder_id: UUID,
    ) -> Link:
        new_link = Link(
            user_id=user_id,
            name=name,
            original_url=original_url,
            short_code=short_code,
            folder_id=folder_id,
        )
        self.session.add(new_link)
        await self.session.flush()
        await self.session.refresh(new_link)
        return new_link

    async def get_by_id(self, link_id: UUID) -> Link | None:
        stmt = select(Link).where(Link.link_id == link_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_short_code(self, short_code: str) -> Link | None:
        stmt = select(Link).where(Link.short_code == short_code)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def update(self, link_id: UUID, **kwargs) -> Link | None:
        stmt = update(Link).where(Link.link_id == link_id).values(**kwargs)
        res = await self.session.execute(stmt.returning(Link))
        return res.scalar_one_or_none()

    async def delete(self, link_id: UUID) -> UUID | None:
        stmt = delete(Link).where(Link.link_id == link_id)
        res = await self.session.execute(stmt.returning(Link.link_id))
        return res.scalar_one_or_none()
