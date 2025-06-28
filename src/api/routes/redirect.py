import json

from api.utils.redirect.decorators import RedirectDecorators
from core.cache.redis.client import redis_client
from core.db.session import get_db
from db.models import Link
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from services.cache_producers.redirect import RedirectCacheProducer
from services.db_producers.link import LinkDBProducer
from sqlalchemy.ext.asyncio import AsyncSession


redirect_router = APIRouter()


@redirect_router.get("/{short_link}")
@RedirectDecorators.check_link_available
async def get_link_by_reduced(
    short_link: str,
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    link_producer = LinkDBProducer(session=db)
    redirect_cache_producer = RedirectCacheProducer(redis_client=redis_client)
    if cached_link := await redirect_cache_producer._get_link_from_cache(short_link):
        link = Link(**cached_link)
    else:
        link = await link_producer._get_link_by_reduced(short_link)
    if not link.entry_link:
        raise HTTPException(status_code=404, detail="Entry link not found.")
    if link.clicks >= 10:
        raise HTTPException(status_code=406, detail="Limit of link uses exceeded.")
    updated_clicks = {"clicks": link.clicks + 1}
    updated_link = await link_producer._update_link(link.link_id, updated_clicks)
    await redirect_cache_producer.update_link_in_cache(updated_link)
    return RedirectResponse(url=link.entry_link)
