from uuid import UUID

from src.links.core.base_componenets.repositories.link.db import ILinkRepository
from src.links.core.domain.schemas.inner.link import LinkResponseInner


class GetLinkByIdUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(self, link_id: UUID) -> LinkResponseInner:
        link = await self.repo.get_by_id(link_id)
        return link
