from uuid import UUID

from src.users.core.base_componenets.repositories.db import IUserRepository
from src.users.core.domain.schemas.inner.user import UserResponseInner


class GetUserByIdUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, user_id: UUID) -> UserResponseInner:
        user = await self.repo.get_by_id(user_id)
        return user
