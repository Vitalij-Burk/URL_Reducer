from uuid import UUID

from src.users.core.base_componenets.repositories.db import IUserRepository
from src.users.core.domain.schemas.inner.user import DeletedUserResponseInner


class DeleteUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, user_id: UUID) -> DeletedUserResponseInner:
        deleted_user_resp = await self.repo.delete(user_id)
        return deleted_user_resp
