from uuid import UUID

from src.core.base_componenets.repositories.db.link import ILinkRepository
from src.core.domain.schemas.dataclasses.link import DeletedLinkResponseInner


class DeleteLinkUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(self, link_id: UUID) -> DeletedLinkResponseInner:
        resp = await self.repo.delete(link_id)
        return resp
