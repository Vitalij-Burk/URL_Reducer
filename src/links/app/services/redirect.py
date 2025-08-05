from fastapi.responses import RedirectResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.links.core.use_cases.redirect.redirect import RedirectUseCase
from src.links.infrastructure.storages.link_repository_manager import (
    LinkRepositoryManager,
)


class RedirectService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.link_manager = LinkRepositoryManager(db, client)
        self.redirect_use_case = RedirectUseCase(self.link_manager)

    async def redirect(self, short_code: str) -> RedirectResponse:
        url = await self.redirect_use_case.execute(short_code)
        return RedirectResponse(url)
