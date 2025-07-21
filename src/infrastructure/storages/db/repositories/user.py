import json
from dataclasses import asdict
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_componenets.repositories.db.user import IUserRepository
from src.core.domain.exceptions.user import UserAlreadyExists
from src.core.domain.exceptions.user import UserNotFound
from src.core.domain.logger import logger
from src.core.domain.schemas.dataclasses.user import CreateUserInner
from src.core.domain.schemas.dataclasses.user import DeletedUserResponseInner
from src.core.domain.schemas.dataclasses.user import UpdateUserRequestInner
from src.core.domain.schemas.dataclasses.user import UserResponseInner
from src.core.utils.serializers.from_orm.user import serialize_to_inner_user
from src.core.utils.serializers.to_dict import serialize_to_dict_exclude_none
from src.infrastructure.storages.db.dal.user import UserDAL


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.user_dal = UserDAL(session)

    async def create(self, entity: CreateUserInner) -> UserResponseInner:
        try:
            new_user = await self.user_dal.create(**asdict(entity))
            return serialize_to_inner_user(new_user)
        except IntegrityError as err:
            logger.error(err)
            raise UserAlreadyExists(str(entity.email))

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
        print(serialize_to_dict_exclude_none(update_user_params))
        user = await self.user_dal.update(
            id, **serialize_to_dict_exclude_none(update_user_params)
        )
        if not user:
            raise UserNotFound(id)
        return serialize_to_inner_user(user)

    async def delete(self, id: UUID) -> DeletedUserResponseInner | None:
        deleted_user_id = await self.user_dal.delete(id)
        return DeletedUserResponseInner(deleted_user_id=deleted_user_id)
