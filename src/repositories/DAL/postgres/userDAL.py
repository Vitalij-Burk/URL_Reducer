from uuid import UUID

from db.models import User
from repositories.DAL.postgres.utils.decorators import DALDecorators
from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, name: str, email: str, hashed_password: str) -> User:
        new_user = User(name=name, email=email, hashed_password=hashed_password)
        self.db_session.add(new_user)
        await self.db_session.flush()
        await self.db_session.refresh(new_user)
        await self.db_session.commit()
        return new_user

    @DALDecorators.execute_query
    async def get_user_by_id(self, user_id: UUID):
        return (
            select(User)
            .where(User.user_id == user_id)
            .options(selectinload(User.links))
        )

    @DALDecorators.execute_query
    async def get_user_by_email(self, email: str):
        return select(User).where(User.email == email).options(selectinload(User.links))

    @DALDecorators.execute_query
    async def update_user(self, user_id: UUID, **kwargs):
        return (
            update(User).where(User.user_id == user_id).values(**kwargs).returning(User)
        )

    @DALDecorators.execute_query
    async def delete_user(self, user_id: UUID):
        return delete(User).where(User.user_id == user_id).returning(User.user_id)
