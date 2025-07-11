from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.models import Link


class LinkDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, user_id: UUID, name: str, entry_link: str, short_link: str
    ) -> Link:
        new_link = Link(
            user_id=user_id,
            name=name,
            entry_link=entry_link,
            short_link=short_link,
        )
        self.session.add(new_link)
        await self.session.flush()
        await self.session.refresh(new_link)
        return new_link

    async def get_by_id(self, link_id: UUID) -> Link | None:
        query = select(Link).where(Link.link_id == link_id)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def get_by_reduced(self, short_link: str) -> Link | None:
        query = select(Link).where(Link.short_link == short_link)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def update(self, link_id: UUID, **kwargs) -> Link | None:
        query = (
            update(Link).where(Link.link_id == link_id).values(**kwargs).returning(Link)
        )
        res = await self.session.execute(query)
        return res.scalar_one_or_none()

    async def delete(self, link_id: UUID) -> UUID | None:
        query = delete(Link).where(Link.link_id == link_id).returning(Link.link_id)
        res = await self.session.execute(query)
        return res.scalar_one_or_none()
