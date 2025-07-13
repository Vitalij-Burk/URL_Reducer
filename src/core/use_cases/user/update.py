from uuid import UUID

from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.schemas.general.user import UpdateUserRequest
from src.core.domain.schemas.safe.user import UserResponse
from src.core.utils.serializers.from_pydantic.user import pydantic_inner_user_to_safe


class UpdateUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, user_id: UUID, body: UpdateUserRequest) -> UserResponse:
        updated_user = await self.repo.update(user_id, body.model_dump())
        return pydantic_inner_user_to_safe(updated_user)
