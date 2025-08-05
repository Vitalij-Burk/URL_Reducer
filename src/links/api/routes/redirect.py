from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import RedirectResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.links.app.services.redirect import RedirectService
from src.links.infrastructure.storages.cache.base.client import get_redis_client
from src.links.infrastructure.storages.db.base.session import get_db


redirect_router = APIRouter()


@redirect_router.get("/{short_code}")
async def redirect(
    short_code: str,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> RedirectResponse:
    redirect_service = RedirectService(db, client)
    redirect_response = await redirect_service.redirect(short_code=short_code)
    return redirect_response
