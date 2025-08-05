from uuid import UUID

from src.links.core.base_componenets.repositories.link.db import ILinkRepository
from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.core.domain.schemas.inner.link import UpdateLinkRequestInner


class UpdateLinkUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(
        self, link_id: UUID, update_link_params: UpdateLinkRequestInner
    ) -> LinkResponseInner:
        updated_link = await self.repo.update(link_id, update_link_params)
        return updated_link
