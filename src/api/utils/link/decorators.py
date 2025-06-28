from functools import wraps
from uuid import UUID

from core.api.errors import ForbiddenError
from core.cache.redis.client import redis_client
from db.models import User
from fastapi import HTTPException
from models.schemas.link import ShowLink
from services.cache_producers.link import LinkCacheProducer
from services.db_producers.link import LinkDBProducer
from sqlalchemy.ext.asyncio import AsyncSession


class LinkDecorators:
    @staticmethod
    def check_user_ownership(func):
        @wraps(func)
        async def wrapper(
            link_id: UUID, current_user: User, db: AsyncSession, *args, **kwargs
        ):
            link_db_producer = LinkDBProducer(session=db)
            link_cache_producer = LinkCacheProducer(redis_client=redis_client)
            if link := await link_cache_producer._get_link_from_cache(link_id):
                link = ShowLink(**link)
            else:
                link = await link_db_producer._get_link_by_id(link_id)
            if current_user.user_id != link.user_id:
                raise ForbiddenError
            return await func(
                link_id=link_id, current_user=current_user, db=db, *args, **kwargs
            )

        return wrapper

    @staticmethod
    def check_link_available(func):
        @wraps(func)
        async def wrapper(link_id: UUID, db: AsyncSession, *args, **kwargs):
            link_db_producer = LinkDBProducer(session=db)
            link_cache_producer = LinkCacheProducer(redis_client=redis_client)
            if not await link_cache_producer._get_link_from_cache(link_id):
                if not await link_db_producer._get_link_by_id(link_id):
                    raise HTTPException(
                        status_code=404, detail=f"Link with id <{link_id}> not found."
                    )
            return await func(link_id=link_id, db=db, *args, **kwargs)

        return wrapper
