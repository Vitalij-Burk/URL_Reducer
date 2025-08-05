from dataclasses import asdict
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain import logger
from src.core.utils.serializers.to_dict import serialize_to_dict_exclude_none
from src.links.core.base_componenets.repositories.link.db import ILinkRepository
from src.links.core.domain.exceptions.link import LinkAlreadyExists
from src.links.core.domain.exceptions.link import LinkNotFound
from src.links.core.domain.schemas.inner.link import CreateLinkRequestInner
from src.links.core.domain.schemas.inner.link import DeletedLinkResponseInner
from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.core.domain.schemas.inner.link import MoveLinkRequestInner
from src.links.core.domain.schemas.inner.link import UpdateLinkRequestInner
from src.links.core.utils.serializers.link.from_orm import serialize_to_inner_link
from src.links.infrastructure.storages.db.base.DAL.link import LinkDAL


class LinkRepository(ILinkRepository):
    def __init__(self, session: AsyncSession):
        self.link_dal = LinkDAL(session)

    async def create(self, entity: CreateLinkRequestInner) -> LinkResponseInner:
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

    async def move(
        self, id: UUID, move_link_params: MoveLinkRequestInner
    ) -> LinkResponseInner | None:
        link = await self.link_dal.update(id, **asdict(move_link_params))
        if not link:
            raise LinkNotFound(id)
        return serialize_to_inner_link(link)

    async def delete(self, id: UUID) -> DeletedLinkResponseInner | None:
        deleted_link_id = await self.link_dal.delete(id)
        return DeletedLinkResponseInner(deleted_link_id=deleted_link_id)
