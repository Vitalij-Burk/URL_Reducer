from uuid import UUID

from db.models import Link
from repositories.DAL.postgres.utils.decorators import DALDecorators
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession


class LinkDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_link(
        self, user_id: UUID, name: str, entry_link: str, short_link: str
    ):
        new_link = Link(
            user_id=user_id,
            name=name,
            entry_link=entry_link,
            short_link=short_link,
        )
        self.db_session.add(new_link)
        await self.db_session.flush()
        await self.db_session.refresh(new_link)
        await self.db_session.commit()
        return new_link

    @DALDecorators.execute_query
    async def get_link_by_id(self, link_id: UUID):
        return select(Link).where(Link.link_id == link_id)

    @DALDecorators.execute_query_all
    async def get_links_by_user_id(self, user_id: UUID):
        return select(Link).where(Link.user_id == user_id)

    @DALDecorators.execute_query
    async def get_link_by_reduced(self, short_link: str):
        return select(Link).where(Link.short_link == short_link)

    @DALDecorators.execute_query
    async def update_link(self, link_id: UUID, **kwargs):
        return (
            update(Link).where(Link.link_id == link_id).values(**kwargs).returning(Link)
        )

    @DALDecorators.execute_query
    async def delete_link(self, link_id: UUID):
        return delete(Link).where(Link.link_id == link_id).returning(Link.link_id)
