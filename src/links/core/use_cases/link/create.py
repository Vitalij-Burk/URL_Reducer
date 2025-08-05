from src.links.core.base_componenets.repositories.link.db import ILinkRepository
from src.links.core.domain.schemas.inner.link import CreateLinkRequestInner
from src.links.core.domain.schemas.inner.link import LinkResponseInner


class CreateLinkUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(self, dto: CreateLinkRequestInner) -> LinkResponseInner:
        link = await self.repo.create(dto)
        return link
