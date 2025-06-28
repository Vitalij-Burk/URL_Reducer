import json
from logging import getLogger
from uuid import UUID

from api.utils.user.decorators import UserDecorators
from core.cache.redis.client import redis_client
from db.models import User
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from models.schemas.user import CreateUser
from models.schemas.user import DeletedUserResponse
from models.schemas.user import ShowUser
from models.schemas.user import UpdateUserRequest
from services.cache_producers.user import UserCacheProducer
from services.db_producers.user import UserDBProducer
from services.utils.auth import get_current_user_from_token
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.session import get_db


user_router = APIRouter()


logger = getLogger(__name__)


@user_router.post("/", response_model=ShowUser)
async def create_user(body: CreateUser, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        user_db_producer = UserDBProducer(session=db)
        # user_cache_producer = UserCacheProducer(redis_client=redis_client)
        user = await user_db_producer._create_user(body)
        # await user_cache_producer._cache_user(user)
        return user
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}.")


@user_router.get("/id/{user_id}", response_model=ShowUser)
@UserDecorators.check_user_ownership
@UserDecorators.check_user_available
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user_db_producer = UserDBProducer(session=db)
    user_cache_producer = UserCacheProducer(redis_client=redis_client)
    # if user_from_cache := await user_cache_producer._get_user_from_cache(user_id):
    #     return user_from_cache
    user = await user_db_producer._get_user_by_id(user_id)
    # await user_cache_producer._cache_user(user)
    return user


@user_router.get("/email/{email}", response_model=ShowUser)
# @UserDecorators.check_user_ownership
# @UserDecorators.check_user_available
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user_db_producer = UserDBProducer(session=db)
    user_cache_producer = UserCacheProducer(redis_client=redis_client)
    # if user_from_cache := await user_cache_producer._get_user_from_cache(email):
    #     return user_from_cache
    user = await user_db_producer._get_user_by_email(email=email)
    # await user_cache_producer._cache_user(user)
    return user


@user_router.patch("/{user_id}", response_model=ShowUser)
@UserDecorators.check_user_ownership
@UserDecorators.check_user_available
async def update_user(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    updated_user_params = body.model_dump(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter should be provided for user update",
        )
    user_db_producer = UserDBProducer(session=db)
    user_cache_producer = UserCacheProducer(redis_client=redis_client)
    updated_user = await user_db_producer._update_user(user_id, updated_user_params)
    await user_cache_producer.update_user_in_cache(user_id, updated_user)
    return updated_user


@user_router.delete("/{user_id}", response_model=DeletedUserResponse)
@UserDecorators.check_user_ownership
@UserDecorators.check_user_available
async def update_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeletedUserResponse:
    user_db_producer = UserDBProducer(session=db)
    user_cache_producer = UserCacheProducer(redis_client=redis_client)
    deleted_user_id = await user_db_producer._delete_user(user_id)
    await user_cache_producer._delete_user_from_cache(user_id)
    return DeletedUserResponse(deleted_user_id=deleted_user_id)
