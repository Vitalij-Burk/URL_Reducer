from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.http_errors import NotFoundError
from src.core.domain.schemas.general.user import DeletedUserResponse
from src.core.domain.schemas.inner.user import CreateUserInner
from src.core.domain.schemas.inner.user import UserResponseInner
from src.core.repositories.db.user import IUserRepository
from src.core.utils.serializers.from_orm.user import db_user_to_pydantic_inner_user
from src.infrastructure.storages.db.dal.user import UserDAL


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.user_dal = UserDAL(session)

    async def create(self, user: CreateUserInner) -> UserResponseInner:
        new_user = await self.user_dal.create(**user.model_dump())
        return db_user_to_pydantic_inner_user(new_user)

    async def get_by_id(self, id: UUID) -> UserResponseInner | None:
        user = await self.user_dal.get_by_id(id)
        if not user:
            raise NotFoundError
        return db_user_to_pydantic_inner_user(user)

    async def get_by_email(self, email: str) -> UserResponseInner | None:
        user = await self.user_dal.get_by_email(email)
        if not user:
            raise NotFoundError
        return db_user_to_pydantic_inner_user(user)

    async def update(
        self, id: UUID, update_user_params: dict
    ) -> UserResponseInner | None:
        user = await self.user_dal.update(id, **update_user_params)
        if not user:
            raise NotFoundError
        return db_user_to_pydantic_inner_user(user)

    async def delete(self, id: UUID) -> DeletedUserResponse | None:
        deleted_user_id = await self.user_dal.delete(id)
        return DeletedUserResponse(deleted_user_id=deleted_user_id)
