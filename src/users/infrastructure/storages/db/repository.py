from dataclasses import asdict
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.logger import app_logger
from src.core.utils.serializers.to_dict import serialize_to_dict_exclude_none
from src.users.core.base_componenets.repositories.db import IUserRepository
from src.users.core.domain.exceptions.user import UserNotFound
from src.users.core.domain.exceptions.user import UserParams
from src.users.core.domain.schemas.inner.user import CreateUserRequestInner
from src.users.core.domain.schemas.inner.user import DeletedUserResponseInner
from src.users.core.domain.schemas.inner.user import UpdateUserRequestInner
from src.users.core.domain.schemas.inner.user import UserResponseInner
from src.users.core.utils.serializers.from_orm import serialize_to_inner_user
from src.users.infrastructure.storages.db.base.DAL import UserDAL


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.user_dal = UserDAL(session)

    async def create(self, entity: CreateUserRequestInner) -> UserResponseInner:
        try:
            new_user = await self.user_dal.create(**asdict(entity))
            return serialize_to_inner_user(new_user)
        except IntegrityError as err:
            app_logger.error(err)
            raise UserParams

    async def get_by_id(self, id: UUID) -> UserResponseInner | None:
        user = await self.user_dal.get_by_id(id)
        if not user:
            raise UserNotFound(id)
        return serialize_to_inner_user(user)

    async def get_by_email(self, email: str) -> UserResponseInner | None:
        user = await self.user_dal.get_by_email(email)
        if not user:
            raise UserNotFound(email)
        return serialize_to_inner_user(user)

    async def update(
        self, id: UUID, update_user_params: UpdateUserRequestInner
    ) -> UserResponseInner | None:
        user = await self.user_dal.update(
            id, **serialize_to_dict_exclude_none(update_user_params)
        )
        if not user:
            raise UserNotFound(id)
        return serialize_to_inner_user(user)

    async def delete(self, id: UUID) -> DeletedUserResponseInner | None:
        deleted_user_id = await self.user_dal.delete(id)
        return DeletedUserResponseInner(deleted_user_id=deleted_user_id)
