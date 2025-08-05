from uuid import UUID

from src.links.core.base_componenets.repositories.link.db import ILinkRepository
from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.core.domain.schemas.inner.link import MoveLinkRequestInner


class MoveLinkUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(
        self, link_id: UUID, move_link_params: MoveLinkRequestInner
    ) -> LinkResponseInner:
        moved_link = await self.repo.move(link_id, move_link_params)
        return moved_link
