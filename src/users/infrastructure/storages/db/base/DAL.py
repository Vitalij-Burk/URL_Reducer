from uuid import UUID

from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.users.infrastructure.storages.db.base.models import User


class UserDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, name: str, email: str, hashed_password: str) -> User:
        new_user = User(name=name, email=email, hashed_password=hashed_password)
        self.session.add(new_user)
        await self.session.flush()
        await self.session.refresh(new_user)
        return new_user

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        res = await self.session.execute(
            stmt.options(selectinload(User.links), selectinload(User.folders))
        )
        return res.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        res = await self.session.execute(
            stmt.options(selectinload(User.links), selectinload(User.folders))
        )
        return res.scalar_one_or_none()

    async def update(self, user_id: UUID, **kwargs) -> User | None:
        stmt = update(User).where(User.user_id == user_id).values(**kwargs)
        res = await self.session.execute(stmt.returning(User))
        return res.scalar_one_or_none()

    async def delete(self, user_id: UUID) -> UUID | None:
        stmt = delete(User).where(User.user_id == user_id)
        res = await self.session.execute(stmt.returning(User.user_id))
        return res.scalar_one_or_none()
