from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_componenets.repositories.db.link import ILinkRepository
from src.core.domain.http_errors import NotFoundError
from src.core.domain.schemas.general.link import DeletedLinkResponse
from src.core.domain.schemas.inner.link import CreateLinkInner
from src.core.domain.schemas.inner.link import LinkResponseInner
from src.core.utils.serializers.from_orm.link import db_link_to_pydantic_inner_link
from src.infrastructure.storages.db.dal.link import LinkDAL


class LinkRepository(ILinkRepository):
    def __init__(self, session: AsyncSession):
        self.link_dal = LinkDAL(session)

    async def create(self, entity: CreateLinkInner) -> LinkResponseInner:
        new_link = await self.link_dal.create(**entity.model_dump())
        return db_link_to_pydantic_inner_link(new_link)

    async def get_by_id(self, id: UUID) -> LinkResponseInner | None:
        link = await self.link_dal.get_by_id(id)
        if not link:
            raise NotFoundError
        return db_link_to_pydantic_inner_link(link)

    async def get_by_short_code(self, short_code: str) -> LinkResponseInner | None:
        link = await self.link_dal.get_by_short_code(short_code)
        if not link:
            raise NotFoundError
        return db_link_to_pydantic_inner_link(link)

    async def update(
        self, id: UUID, update_link_params: dict
    ) -> LinkResponseInner | None:
        link = await self.link_dal.update(id, **update_link_params)
        if not link:
            raise NotFoundError
        return db_link_to_pydantic_inner_link(link)

    async def delete(self, id: UUID) -> DeletedLinkResponse | None:
        deleted_link_id = await self.link_dal.delete(id)
        return DeletedLinkResponse(deleted_link_id=deleted_link_id)
