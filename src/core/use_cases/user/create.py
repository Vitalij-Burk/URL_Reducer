from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.schemas.dataclasses.user import CreateUserInner
from src.core.domain.schemas.dataclasses.user import UserResponseInner
from src.core.interfaces.crypto_provider import ICryptoProvider


class CreateUserUseCase:
    def __init__(self, repo: IUserRepository, hasher: ICryptoProvider):
        self.repo = repo
        self.hasher = hasher

    async def execute(self, dto: CreateUserInner) -> UserResponseInner:
        user = await self.repo.create(dto)
        return user
