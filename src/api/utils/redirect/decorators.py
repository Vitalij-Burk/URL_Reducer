from functools import wraps

from core.cache.redis.client import redis_client
from db.models import Link
from fastapi import HTTPException
from models.schemas.link import ShowLink
from services.cache_producers.redirect import RedirectCacheProducer
from services.db_producers.link import LinkDBProducer
from sqlalchemy.ext.asyncio import AsyncSession


class RedirectDecorators:
    @staticmethod
    def check_link_available(func):
        @wraps(func)
        async def wrapper(short_link: str, db: AsyncSession, *args, **kwargs):
            link_producer = LinkDBProducer(session=db)
            redirect_cache_producer = RedirectCacheProducer(redis_client=redis_client)
            if cached_link := await redirect_cache_producer._get_link_from_cache(
                short_link
            ):
                link = Link(**cached_link)
            else:
                link = await link_producer._get_link_by_reduced(short_link)
            if not link.entry_link:
                raise HTTPException(
                    status_code=404,
                    detail=f"Entry link with short link <{short_link}> not found.",
                )
            return await func(short_link=short_link, db=db, *args, **kwargs)

        return wrapper
