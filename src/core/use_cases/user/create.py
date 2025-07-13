from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.schemas.safe.user import CreateUser
from src.core.domain.schemas.safe.user import UserResponse
from src.core.interfaces.password_hasher import IPassword
from src.core.utils.serializers.from_pydantic.user import pydantic_create_user_to_inner
from src.core.utils.serializers.from_pydantic.user import pydantic_inner_user_to_safe


class CreateUserUseCase:
    def __init__(self, repo: IUserRepository, hasher: IPassword):
        self.repo = repo
        self.hasher = hasher

    async def execute(self, dto: CreateUser) -> UserResponse:
        password_hash = self.hasher.get_password_hash(dto.password)
        inner = pydantic_create_user_to_inner(dto, password_hash)
        user = await self.repo.create(inner)
        return pydantic_inner_user_to_safe(user)
