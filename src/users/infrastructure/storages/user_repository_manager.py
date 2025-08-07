import asyncio
from uuid import UUID

import redis.exceptions
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.exceptions.base import AppError
from src.core.domain.logger import app_logger
from src.users.core.base_componenets.repositories.db import IUserRepository
from src.users.core.domain.schemas.inner.user import CreateUserRequestInner
from src.users.core.domain.schemas.inner.user import DeletedUserResponseInner
from src.users.core.domain.schemas.inner.user import UpdateUserRequestInner
from src.users.core.domain.schemas.inner.user import UserResponseInner
from src.users.infrastructure.storages.cache.unit_of_work import (
    UnitOfWork as CacheUnitOfWork,
)
from src.users.infrastructure.storages.db.unit_of_work import UnitOfWork as DBUnitOfWork


class UserRepositoryManager(IUserRepository):
    def __init__(self, session: AsyncSession, client: Redis):
        self.db_uow = DBUnitOfWork(session)
        self.cache_uow = CacheUnitOfWork(client)

    async def _cache_user(self, user: UserResponseInner):
        async with self.cache_uow as uow:
            await uow.start_pipeline()
            await uow.users.cache_by_id(user.user_id, user)
            await uow.users.cache_by_email(user.email, user)

    async def _delete_cached_user(self, user: UserResponseInner):
        async with self.cache_uow as uow:
            await uow.start_pipeline()
            await uow.users.delete_by_id(user.user_id)
            await uow.users.delete_by_email(user.email)

    async def create(self, entity: CreateUserRequestInner) -> UserResponseInner:
        async with self.db_uow as uow:
            user = await uow.users.create(entity)
        return user

    async def get_by_id(self, id: UUID) -> UserResponseInner | None:
        user = None
        try:
            user = await self.cache_uow.users.get_by_id(id)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        except AppError as err:
            app_logger.info(f"Cache access error: '{err}'")

        if user is not None:
            return user

        async with self.db_uow as uow:
            user = await uow.users.get_by_id(id)

        if user is not None:
            try:
                await self._cache_user(user)
            except (
                redis.exceptions.ConnectionError,
                redis.exceptions.TimeoutError,
            ) as err:
                app_logger.error(f"Redis folder connection error: '{err}'")
            except AppError as err:
                app_logger.error(f"Cache set error: {err}")

        return user

    async def get_by_email(self, email: str) -> UserResponseInner | None:
        user = None
        try:
            user = await self.cache_uow.users.get_by_email(email)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        except AppError as err:
            app_logger.info(f"Cache access error: '{err}'")

        if user is not None:
            return user

        async with self.db_uow as uow:
            user = await uow.users.get_by_email(email)

        if user is not None:
            try:
                await self._cache_user(user)
            except (
                redis.exceptions.ConnectionError,
                redis.exceptions.TimeoutError,
            ) as err:
                app_logger.error(f"Redis folder connection error: '{err}'")
            except AppError as err:
                app_logger.error(f"Cache setting error: '{err}'")

        return user

    async def update(
        self, id: UUID, update_user_params: UpdateUserRequestInner
    ) -> UserResponseInner | None:
        async with self.db_uow as uow:
            user = await uow.users.update(id, update_user_params)
        try:
            await self._delete_cached_user(user)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        finally:
            return user

    async def delete(self, id: UUID) -> DeletedUserResponseInner | None:
        async with self.db_uow as uow:
            user = await uow.users.get_by_id(id)
        try:
            await self._delete_cached_user(user)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as err:
            app_logger.error(f"Redis folder connection error: '{err}'")
        finally:
            async with self.db_uow as uow:
                deleted_user_response = await uow.users.delete(id)
            return deleted_user_response
