from dataclasses import asdict
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_componenets.repositories.db.link import ILinkRepository
from src.core.domain import logger
from src.core.domain.exceptions.link import LinkAlreadyExists
from src.core.domain.exceptions.link import LinkNotFound
from src.core.domain.schemas.dataclasses.link import CreateLinkInner
from src.core.domain.schemas.dataclasses.link import DeletedLinkResponseInner
from src.core.domain.schemas.dataclasses.link import LinkResponseInner
from src.core.domain.schemas.dataclasses.link import UpdateLinkRequestInner
from src.core.utils.serializers.from_orm.link import serialize_to_inner_link
from src.core.utils.serializers.to_dict import serialize_to_dict_exclude_none
from src.infrastructure.storages.db.dal.link import LinkDAL


class LinkRepository(ILinkRepository):
    def __init__(self, session: AsyncSession):
        self.link_dal = LinkDAL(session)

    async def create(self, entity: CreateLinkInner) -> LinkResponseInner:
        try:
            new_link = await self.link_dal.create(**asdict(entity))
            return serialize_to_inner_link(new_link)
        except IntegrityError as err:
            logger.error(err)
            raise LinkAlreadyExists(str(entity))

    async def get_by_id(self, id: UUID) -> LinkResponseInner | None:
        link = await self.link_dal.get_by_id(id)
        if not link:
            raise LinkNotFound(id)
        return serialize_to_inner_link(link)

    async def get_by_short_code(self, short_code: str) -> LinkResponseInner | None:
        link = await self.link_dal.get_by_short_code(short_code)
        if not link:
            raise LinkNotFound(short_code)
        return serialize_to_inner_link(link)

    async def update(
        self, id: UUID, update_link_params: UpdateLinkRequestInner
    ) -> LinkResponseInner | None:
        link = await self.link_dal.update(
            id, **serialize_to_dict_exclude_none(update_link_params)
        )
        if not link:
            raise LinkNotFound(id)
        return serialize_to_inner_link(link)

    async def delete(self, id: UUID) -> DeletedLinkResponseInner | None:
        deleted_link_id = await self.link_dal.delete(id)
        return DeletedLinkResponseInner(deleted_link_id=deleted_link_id)
