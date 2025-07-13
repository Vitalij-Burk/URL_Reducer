from uuid import UUID

from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.schemas.general.user import DeletedUserResponse


class DeleteUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, user_id: UUID) -> DeletedUserResponse:
        deleted_user_resp = await self.repo.delete(user_id)
        return deleted_user_resp
