from datetime import timedelta
from typing import AsyncGenerator
from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.settings import Config
from core.utils.auth import AccessToken
from models.schemas.user import CreateUser
from services.db_producers.user import UserDBProducer

TABLES_FOR_CLEANING = ["links", "users"]

engine = create_async_engine(
    Config.TEST_DB_URL, future=True, echo=True, poolclass=NullPool)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def test_app():
    """Фикстура приложения с переопределенными зависимостями для тестов"""
    from src.main import app
    from src.core.db.session import get_db

    # Переопределяем зависимости
    app.dependency_overrides[get_db] = get_test_db

    yield app

    # Очищаем переопределения после теста
    app.dependency_overrides.clear()


async def get_test_db() -> AsyncGenerator[AsyncSession, None]:
    session = async_session()
    try:
        for table in TABLES_FOR_CLEANING:
            await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
        await session.commit()
        yield session
    finally:
        for table in TABLES_FOR_CLEANING:
            await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
        await session.commit()
        await session.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    session = async_session()
    try:
        for table in TABLES_FOR_CLEANING:
            await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
        await session.commit()
        yield session
    finally:
        for table in TABLES_FOR_CLEANING:
            await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
        await session.commit()
        await session.close()


@pytest.fixture
def test_user():
    return {"name": "name", "email": "name@email.com", "password": "password"}


async def create_user_in_db(
    db_session: AsyncSession, name: str, email: str, password: str
) -> dict:
    user_producer = UserDBProducer(db_session)
    user = await user_producer._create_user(
        CreateUser(name=name, email=email, password=password)
    )
    return user.__dict__


async def get_user_from_db(db_session: AsyncSession, user_id: str) -> dict:
    user_producer = UserDBProducer(db_session)
    user = await user_producer._get_user_by_id(UUID(user_id))
    if user is None:
        raise ValueError(f"User with id {user_id} not found in database")
    return user.__dict__


def create_access_token_for_test(email: str):
    access_token = AccessToken.create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"Authorization": f"Bearer {access_token}"}
