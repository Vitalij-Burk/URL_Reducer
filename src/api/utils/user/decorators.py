from functools import wraps
from uuid import UUID

from core.api.errors import ForbiddenError
from core.cache.redis.client import redis_client
from db.models import User
from fastapi import HTTPException
from services.cache_producers.user import UserCacheProducer
from services.db_producers.user import UserDBProducer
from sqlalchemy.ext.asyncio import AsyncSession


class UserDecorators:
    @staticmethod
    def check_user_ownership(func):
        @wraps(func)
        async def wrapper(user_id: UUID, current_user: User, *args, **kwargs):
            if current_user.user_id != user_id:
                raise ForbiddenError
            return await func(
                user_id=user_id, current_user=current_user, *args, **kwargs
            )

        return wrapper

    @staticmethod
    def check_user_available(func):
        @wraps(func)
        async def wrapper(user_id: UUID, db: AsyncSession, *args, **kwargs):
            user_db_producer = UserDBProducer(session=db)
            user_cache_producer = UserCacheProducer(redis_client=redis_client)
            if not await user_cache_producer._get_user_from_cache(user_id):
                if not await user_db_producer._get_user_by_id(user_id):
                    raise HTTPException(
                        status_code=404, detail=f"User with id <{user_id}> not found."
                    )
            return await func(user_id=user_id, db=db, *args, **kwargs)

        return wrapper
