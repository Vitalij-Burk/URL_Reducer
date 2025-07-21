from uuid import UUID

from src.core.domain.exceptions.user import UserForbidden
from src.core.domain.schemas.pydantic.user import UserResponse
from src.infrastructure.storages.manager.user_repository_manager import (
    UserRepositoryManager,
)


class UserGuard:
    def __init__(self, user_manager: UserRepositoryManager):
        self.user_manager = user_manager

    async def check_user_ownership_by_id(
        self, user_id: UUID, current_user: UserResponse
    ):
        if user_id != current_user.user_id:
            raise UserForbidden(current_user.user_id, user_id)

    async def check_user_ownership_by_email(
        self, email: str, current_user: UserResponse
    ):
        if email != current_user.email:
            raise UserForbidden(current_user.email, email)
