from uuid import UUID

from src.core.domain.http_errors import ForbiddenError
from src.core.domain.schemas.safe.user import UserResponse
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
            raise ForbiddenError

    async def check_user_ownership_by_email(
        self, email: str, current_user: UserResponse
    ):
        if email != current_user.email:
            raise ForbiddenError
