from uuid import UUID

from src.users.core.base_componenets.repositories.db import IUserRepository
from src.users.core.domain.schemas.inner.user import UpdateUserRequestInner
from src.users.core.domain.schemas.inner.user import UserResponseInner


class UpdateUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(
        self, user_id: UUID, update_user_params: UpdateUserRequestInner
    ) -> UserResponseInner:
        updated_user = await self.repo.update(user_id, update_user_params)
        return updated_user
