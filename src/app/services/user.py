from uuid import UUID

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.decorators.user import check_user_ownership_by_email
from src.app.decorators.user import check_user_ownership_by_id
from src.app.guards.user import UserGuard
from src.core.domain.logger import logger
from src.core.domain.schemas.general.user import DeletedUserResponse
from src.core.domain.schemas.general.user import UpdateUserRequest
from src.core.domain.schemas.safe.user import CreateUser
from src.core.domain.schemas.safe.user import UserResponse
from src.core.utils.serializers.from_pydantic.user import pydantic_create_user_to_inner
from src.core.utils.serializers.from_pydantic.user import pydantic_inner_user_to_safe
from src.infrastructure.auth.password import Security
from src.infrastructure.storages.manager.user_repository_manager import (
    UserRepositoryManager,
)


class UserService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.user_manager = UserRepositoryManager(db, client)
        self.guard = UserGuard(self.user_manager)

    async def create_user(self, body: CreateUser) -> UserResponse:
        try:
            user = await self.user_manager.create(
                pydantic_create_user_to_inner(
                    body, Security.get_password_hash(body.password)
                )
            )
            return pydantic_inner_user_to_safe(user)
        except IntegrityError as err:
            logger.error(err)
            raise HTTPException(status_code=503, detail=f"Database error: {err}.")

    @check_user_ownership_by_id
    async def get_user_by_id(
        self, user_id: UUID, current_user: UserResponse
    ) -> UserResponse:
        user = await self.user_manager.get_by_id(user_id)
        return pydantic_inner_user_to_safe(user)

    @check_user_ownership_by_email
    async def get_user_by_email(
        self, email: str, current_user: UserResponse
    ) -> UserResponse:
        user = await self.user_manager.get_by_email(email)
        return pydantic_inner_user_to_safe(user)

    @check_user_ownership_by_id
    async def update_user(
        self, user_id: UUID, body: UpdateUserRequest, current_user: UserResponse
    ) -> UserResponse:
        updated_user = await self.user_manager.update(user_id, body.model_dump())
        return pydantic_inner_user_to_safe(updated_user)

    @check_user_ownership_by_id
    async def delete_user(
        self, user_id: UUID, current_user: UserResponse
    ) -> DeletedUserResponse:
        deleted_user_resp = await self.user_manager.delete(user_id)
        return deleted_user_resp
