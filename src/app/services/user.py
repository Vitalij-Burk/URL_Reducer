from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.decorators.user import check_user_ownership_by_email
from src.app.decorators.user import check_user_ownership_by_id
from src.app.guards.user import UserGuard
from src.core.domain.schemas.pydantic.user import CreateUser
from src.core.domain.schemas.pydantic.user import DeletedUserResponse
from src.core.domain.schemas.pydantic.user import UpdateUserRequest
from src.core.domain.schemas.pydantic.user import UserResponse
from src.core.use_cases.user.create import CreateUserUseCase
from src.core.use_cases.user.delete import DeleteUserUseCase
from src.core.use_cases.user.get_by_email import GetUserByEmailUseCase
from src.core.use_cases.user.get_by_id import GetUserByIdUseCase
from src.core.use_cases.user.update import UpdateUserUseCase
from src.core.utils.serializers.from_inner.user import serialize_to_safe_deleted_user
from src.core.utils.serializers.from_inner.user import serialize_to_safe_user
from src.core.utils.serializers.from_safe.user import serialize_to_create_inner_user
from src.core.utils.serializers.from_safe.user import serialize_to_update_inner_user
from src.infrastructure.auth.password_hasher import PasswordHasher
from src.infrastructure.storages.manager.user_repository_manager import (
    UserRepositoryManager,
)


class UserService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.user_manager = UserRepositoryManager(db, client)
        self.guard = UserGuard(self.user_manager)
        self.hasher = PasswordHasher()
        self.create_user_use_case = CreateUserUseCase(
            repo=self.user_manager, hasher=self.hasher
        )
        self.get_user_by_id_use_case = GetUserByIdUseCase(repo=self.user_manager)
        self.get_user_by_email_use_case = GetUserByEmailUseCase(repo=self.user_manager)
        self.update_user_use_case = UpdateUserUseCase(repo=self.user_manager)
        self.delete_user_use_case = DeleteUserUseCase(repo=self.user_manager)

    async def create_user(self, body: CreateUser) -> UserResponse:
        return serialize_to_safe_user(
            await self.create_user_use_case.execute(
                serialize_to_create_inner_user(
                    body, PasswordHasher.create(body.password)
                )
            )
        )

    @check_user_ownership_by_id
    async def get_user_by_id(
        self, user_id: UUID, current_user: UserResponse
    ) -> UserResponse:
        return serialize_to_safe_user(
            await self.get_user_by_id_use_case.execute(user_id)
        )

    @check_user_ownership_by_email
    async def get_user_by_email(
        self, email: str, current_user: UserResponse
    ) -> UserResponse:
        return serialize_to_safe_user(
            await self.get_user_by_email_use_case.execute(email)
        )

    @check_user_ownership_by_id
    async def update_user(
        self, user_id: UUID, body: UpdateUserRequest, current_user: UserResponse
    ) -> UserResponse:
        return serialize_to_safe_user(
            await self.update_user_use_case.execute(
                user_id, serialize_to_update_inner_user(body)
            )
        )

    @check_user_ownership_by_id
    async def delete_user(
        self, user_id: UUID, current_user: UserResponse
    ) -> DeletedUserResponse:
        return serialize_to_safe_deleted_user(
            deleted_user_id=await self.delete_user_use_case.execute(user_id)
        )
