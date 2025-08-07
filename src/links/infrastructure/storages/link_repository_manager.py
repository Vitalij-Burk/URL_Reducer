from uuid import UUID

import redis.exceptions
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.exceptions.base import AppError
from src.core.domain.logger import app_logger
from src.links.core.base_componenets.repositories.link.db import ILinkRepository
from src.links.core.domain.schemas.inner.link import CreateLinkRequestInner
from src.links.core.domain.schemas.inner.link import DeletedLinkResponseInner
from src.links.core.domain.schemas.inner.link import LinkResponseInner
from src.links.core.domain.schemas.inner.link import MoveLinkRequestInner
from src.links.core.domain.schemas.inner.link import UpdateLinkRequestInner
from src.links.infrastructure.storages.cache.unit_of_work import (
    UnitOfWork as CacheUnitOfWork,
)
from src.links.infrastructure.storages.db.unit_of_work import UnitOfWork as DBUnitOfWork


class LinkRepositoryManager(ILinkRepository):
    def __init__(self, session: AsyncSession, client: Redis):
        self.db_uow = DBUnitOfWork(session)
        self.cache_uow = CacheUnitOfWork(client)

    async def _cache_link(self, link: LinkResponseInner):
        async with self.cache_uow as uow:
            await uow.start_pipeline()
            await uow.links.cache_by_id(link.link_id, link)
            await uow.links.cache_by_short_code(link.short_code, link)

    async def _delete_cached_link(self, link: LinkResponseInner):
        async with self.cache_uow as uow:
            await uow.start_pipeline()
            await uow.links.delete_by_id(link.link_id)
            await uow.links.delete_by_short_code(link.short_code)

    async def create(self, entity: CreateLinkRequestInner) -> LinkResponseInner:
        async with self.db_uow as uow:
            return await uow.links.create(entity)

    async def get_by_id(self, id: UUID) -> LinkResponseInner | None:
        link = None
        try:
            link = await self.cache_uow.links.get_by_id(id)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        except AppError as err:
            app_logger.info(f"Cache access error: '{err}'")

        if link is not None:
            return link

        async with self.db_uow as uow:
            link = await uow.links.get_by_id(id)

        if link is not None:
            try:
                await self._cache_link(link)
            except (
                redis.exceptions.ConnectionError,
                redis.exceptions.TimeoutError,
            ) as err:
                app_logger.error(f"Redis folder connection error: '{err}'")
            except AppError as e:
                app_logger.error(f"Cache error: {e}")

        return link

    async def get_by_short_code(self, short_code: str) -> LinkResponseInner | None:
        link = None
        try:
            link = await self.cache_uow.links.get_by_short_code(short_code)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        except AppError as err:
            app_logger.info(f"Cache access error: '{err}'")

        if link is not None:
            return link

        async with self.db_uow as uow:
            link = await uow.links.get_by_short_code(short_code)

        if link is not None:
            try:
                await self._cache_link(link)
            except (
                redis.exceptions.ConnectionError,
                redis.exceptions.TimeoutError,
            ) as err:
                app_logger.error(f"Redis folder connection error: '{err}'")
            except AppError as e:
                app_logger.error(f"Cache error: {e}")

        return link

    async def update(
        self, id: UUID, update_link_params: UpdateLinkRequestInner
    ) -> LinkResponseInner | None:
        async with self.db_uow as uow:
            link = await uow.links.update(id, update_link_params)
        try:
            await self._delete_cached_link(link)
            await self._cache_link(link)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        finally:
            return link

    async def move(
        self, id: UUID, move_link_params: MoveLinkRequestInner
    ) -> LinkResponseInner | None:
        async with self.db_uow as uow:
            link = await uow.links.move(id, move_link_params)
        try:
            await self._delete_cached_link(link)
            await self._cache_link(link)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        finally:
            return link

    async def delete(self, id: UUID) -> DeletedLinkResponseInner | None:
        async with self.db_uow as uow:
            link = await uow.links.get_by_id(id)
        try:
            await self._delete_cached_link(link)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        finally:
            async with self.db_uow as uow:
                deleted_link_response = await self.db_uow.links.delete(id)
            return deleted_link_response
