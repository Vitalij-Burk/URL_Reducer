from uuid import UUID

from src.users.core.domain.exceptions.user import UserForbidden
from src.users.infrastructure.storages.user_repository_manager import (
    UserRepositoryManager,
)


class UserGuard:
    def __init__(self, user_manager: UserRepositoryManager):
        self.user_manager = user_manager

    async def check_user_ownership_by_id(self, user_id: UUID, current_user_id: UUID):
        if user_id != current_user_id:
            raise UserForbidden(current_user_id, user_id)

    async def check_user_ownership_by_email(self, email: str, current_user_email: str):
        if email != current_user_email:
            raise UserForbidden(current_user_email, email)
