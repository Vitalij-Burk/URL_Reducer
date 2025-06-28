from typing import Union
from uuid import UUID

from core.cache.redis.client import redis_client
from db.models import Link
from models.schemas.link import CreateLink
from models.schemas.link import ShowLink
from repositories.DAL.postgres.linkDAL import LinkDAL
from services.utils.get_random_string import get_random_string
from sqlalchemy.ext.asyncio import AsyncSession


class LinkDBProducer:
    def __init__(self, session: AsyncSession):
        self.link_dal = LinkDAL(session)

    async def _create_link(self, user_id: UUID, body: CreateLink) -> ShowLink:
        link = await self.link_dal.create_link(
            user_id=user_id,
            name=body.name,
            entry_link=str(body.entry_link),
            short_link=await get_random_string(),
        )
        if link:
            return ShowLink(
                link_id=link.link_id,
                user_id=link.user_id,
                name=link.name,
                entry_link=link.entry_link,
                short_link=link.short_link,
                clicks=link.clicks,
            )
        else:
            await self._create_link(user_id, body)

    async def _get_link_by_id(self, link_id: UUID) -> Union[Link, None]:
        link = await self.link_dal.get_link_by_id(link_id=link_id)
        return link

    async def _get_links_by_user_id(self, user_id: UUID) -> Union[list[Link], None]:
        links = await self.link_dal.get_links_by_user_id(user_id=user_id)
        return links

    async def _update_link(
        self, link_id: UUID, updated_link_params: dict
    ) -> Union[Link, None]:
        updated_link_row = await self.link_dal.update_link(
            link_id=link_id, **updated_link_params
        )
        if updated_link_row:
            return updated_link_row

    async def _delete_link(self, link_id: UUID) -> Union[UUID, None]:
        deleted_link_id = await self.link_dal.delete_link(link_id=link_id)
        if deleted_link_id:
            return deleted_link_id

    async def _get_link_by_reduced(self, short_link: str) -> Union[Link, None]:
        link = await self.link_dal.get_link_by_reduced(short_link=short_link)
        return link
