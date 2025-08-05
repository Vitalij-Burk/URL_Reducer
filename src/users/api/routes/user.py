from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from pydantic import EmailStr
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.infrastructure.auth.authenticator import get_current_user_from_token
from src.users.app.services.user import UserService
from src.users.core.domain.schemas.out.user import CreateUserRequest
from src.users.core.domain.schemas.out.user import DeletedUserResponse
from src.users.core.domain.schemas.out.user import UpdateUserRequest
from src.users.core.domain.schemas.out.user import UserResponse
from src.users.infrastructure.storages.cache.base.client import get_redis_client
from src.users.infrastructure.storages.db.base.session import get_db


user_router = APIRouter()


@user_router.post("/", response_model=UserResponse)
async def create_user(
    body: CreateUserRequest,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> UserResponse:
    user_service = UserService(db, client)
    user = await user_service.create_user(body=body)
    return user


@user_router.get("/id/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> UserResponse:
    user_service = UserService(db, client)
    user = await user_service.get_user_by_id(
        user_id=user_id, current_user_id=current_user.user_id
    )
    return user


@user_router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: EmailStr,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> UserResponse:
    user_service = UserService(db, client)
    user = await user_service.get_user_by_email(
        email=email, current_user_email=current_user.email
    )
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
    user = await user_service.update_user(
        user_id=user_id, body=body, current_user_id=current_user.user_id
    )
    return user


@user_router.delete("/{user_id}", response_model=DeletedUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> DeletedUserResponse:
    user_service = UserService(db, client)
    user = await user_service.delete_user(
        user_id=user_id, current_user_id=current_user.user_id
    )
    return user
