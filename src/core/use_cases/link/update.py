from uuid import UUID

from src.core.base_componenets.repositories.db.link import ILinkRepository
from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.core.domain.schemas.dataclasses.link import UpdateLinkRequestInner


class UpdateLinkUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(
        self, link_id: UUID, update_link_params: UpdateLinkRequestInner
    ) -> LinkResponseInner:
        updated_link = await self.repo.update(link_id, update_link_params)
        return updated_link
