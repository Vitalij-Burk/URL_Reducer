from uuid import UUID

from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.schemas.safe.user import UserResponse
from src.core.utils.serializers.from_pydantic.user import pydantic_inner_user_to_safe


class GetUserByIdUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, user_id: UUID) -> UserResponse:
        user = await self.repo.get_by_id(user_id)
        return pydantic_inner_user_to_safe(user)
