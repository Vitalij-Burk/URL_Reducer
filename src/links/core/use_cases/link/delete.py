from uuid import UUID

from src.links.core.base_componenets.repositories.link.db import ILinkRepository
from src.links.core.domain.schemas.inner.link import DeletedLinkResponseInner


class DeleteLinkUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(self, link_id: UUID) -> DeletedLinkResponseInner:
        resp = await self.repo.delete(link_id)
        return resp
