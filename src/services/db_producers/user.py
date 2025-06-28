from typing import Union
from uuid import UUID

from core.utils.password import Security
from db.models import User
from models.schemas.user import CreateUser
from models.schemas.user import ShowUser
from repositories.DAL.postgres.userDAL import UserDAL
from sqlalchemy.ext.asyncio import AsyncSession


class UserDBProducer:
    def __init__(self, session: AsyncSession):
        self.user_dal = UserDAL(session)

    async def _create_user(self, body: CreateUser) -> ShowUser:
        user = await self.user_dal.create_user(
            name=body.name,
            email=body.email,
            hashed_password=Security.get_password_hash(body.password),
        )
        return ShowUser(
            user_id=user.user_id, name=user.name, email=user.email, links=[]
        )

    async def _get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        return await self.user_dal.get_user_by_id(user_id=user_id)

    async def _get_user_by_email(self, email: str) -> Union[User, None]:
        return await self.user_dal.get_user_by_email(email=email)

    async def _update_user(
        self, user_id: UUID, updated_user_params: dict
    ) -> Union[User, None]:
        updated_user_row = await self.user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        if updated_user_row:
            return updated_user_row

    async def _delete_user(self, user_id: UUID) -> Union[UUID, None]:
        deleted_user_id = await self.user_dal.delete_user(user_id=user_id)
        if deleted_user_id:
            return deleted_user_id
