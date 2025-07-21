from uuid import UUID

from src.core.base_componenets.repositories.db.link import ILinkRepository
from src.core.domain.schemas.dataclasses.link import LinkResponseInner


class GetLinkByIdUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(self, link_id: UUID) -> LinkResponseInner:
        link = await self.repo.get_by_id(link_id)
        return link
