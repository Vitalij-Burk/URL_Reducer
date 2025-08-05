from src.links.core.base_componenets.repositories.link.db import ILinkRepository
from src.links.core.domain.exceptions.link import LinkLimitExceeded
from src.links.core.domain.schemas.inner.link import UpdateLinkRequestInner


class RedirectUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(self, short_code: str) -> str:
        link = await self.repo.get_by_short_code(short_code)
        if link.clicks >= 10:
            raise LinkLimitExceeded("clicks")
        updated_clicks = UpdateLinkRequestInner(clicks=link.clicks + 1)
        await self.repo.update(link.link_id, updated_clicks)
        return link.original_url
