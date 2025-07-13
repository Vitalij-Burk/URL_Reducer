from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.schemas.safe.user import UserResponse
from src.core.utils.serializers.from_pydantic.user import pydantic_inner_user_to_safe


class GetUserByEmailUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, email: str) -> UserResponse:
        user = await self.repo.get_by_email(email)
        return pydantic_inner_user_to_safe(user)
