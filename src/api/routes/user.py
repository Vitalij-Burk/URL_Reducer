from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from infrastructure.storages.db.session import get_db
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.user import UserService
from src.core.domain.schemas.general.user import DeletedUserResponse
from src.core.domain.schemas.general.user import UpdateUserRequest
from src.core.domain.schemas.safe.user import CreateUser
from src.core.domain.schemas.safe.user import UserResponse
from src.infrastructure.auth.auth import get_current_user_from_token
from src.infrastructure.storages.cache.client import get_redis_client

user_router = APIRouter()


@user_router.post("/", response_model=UserResponse)
async def create_user(
    body: CreateUser,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> UserResponse:
    user_service = UserService(db, client)
    user = await user_service.create_user(body)
    return user


@user_router.get("/id/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> UserResponse:
    user_service = UserService(db, client)
    user = await user_service.get_user_by_id(user_id, current_user)
    return user


@user_router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> UserResponse:
    user_service = UserService(db, client)
    user = await user_service.get_user_by_email(email, current_user)
    return user


@user_router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> UserResponse:
    user_service = UserService(db, client)
    user = await user_service.update_user(user_id, body, current_user)
    return user


@user_router.delete("/{user_id}", response_model=DeletedUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> DeletedUserResponse:
    user_service = UserService(db, client)
    user = await user_service.delete_user(user_id, current_user)
    return user
