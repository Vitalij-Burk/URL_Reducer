from src.users.core.base_componenets.repositories.db import IUserRepository
from src.users.core.domain.schemas.inner.user import UserResponseInner


class GetUserByEmailUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, email: str) -> UserResponseInner:
        user = await self.repo.get_by_email(email)
        return user
