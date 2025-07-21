from src.core.base_componenets.repositories.db.link import ILinkRepository
from src.core.domain.schemas.dataclasses.link import CreateLinkInner
from src.core.domain.schemas.dataclasses.link import LinkResponseInner


class CreateLinkUseCase:
    def __init__(self, repo: ILinkRepository):
        self.repo = repo

    async def execute(self, dto: CreateLinkInner) -> LinkResponseInner:
        link = await self.repo.create(dto)
        return link
