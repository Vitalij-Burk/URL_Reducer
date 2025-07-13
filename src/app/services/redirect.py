from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils.serializers.from_pydantic.link import pydantic_inner_link_to_safe
from src.infrastructure.storages.manager.link_repository_manager import (
    LinkRepositoryManager,
)


class RedirectService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.link_manager = LinkRepositoryManager(db, client)

    async def redirect(self, short_code: str) -> RedirectResponse:
        link = await self.link_manager.get_by_short_code(short_code)
        if link:
            link = pydantic_inner_link_to_safe(link)
        else:
            raise HTTPException(status_code=404, detail="Original URL link not found.")
        if link.clicks >= 10:
            raise HTTPException(status_code=406, detail="Limit of link uses exceeded.")
        updated_clicks = {"clicks": link.clicks + 1}
        await self.link_manager.update(link.link_id, updated_clicks)
        return RedirectResponse(url=link.original_url)
