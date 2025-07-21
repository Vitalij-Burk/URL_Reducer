from uuid import UUID

from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.schemas.dataclasses.user import UpdateUserRequestInner
from src.core.domain.schemas.dataclasses.user import UserResponseInner


class UpdateUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(
        self, user_id: UUID, update_user_params: UpdateUserRequestInner
    ) -> UserResponseInner:
        updated_user = await self.repo.update(user_id, update_user_params)
        return updated_user
