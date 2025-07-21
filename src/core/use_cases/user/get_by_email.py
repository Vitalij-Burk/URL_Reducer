from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.schemas.dataclasses.user import UserResponseInner


class GetUserByEmailUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, email: str) -> UserResponseInner:
        user = await self.repo.get_by_email(email)
        return user
