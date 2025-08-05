from src.auth.core.interfaces.crypto_provider import ICryptoProvider
from src.users.core.base_componenets.repositories.db import IUserRepository
from src.users.core.domain.schemas.inner.user import CreateUserRequestInner
from src.users.core.domain.schemas.inner.user import UserResponseInner


class CreateUserUseCase:
    def __init__(self, repo: IUserRepository, hasher: ICryptoProvider):
        self.repo = repo
        self.hasher = hasher

    async def execute(self, dto: CreateUserRequestInner) -> UserResponseInner:
        user = await self.repo.create(dto)
        return user
