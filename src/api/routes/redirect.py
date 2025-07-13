from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import RedirectResponse
from infrastructure.storages.cache.client import get_redis_client
from infrastructure.storages.db.session import get_db
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.redirect import RedirectService


redirect_router = APIRouter()


@redirect_router.get("/{short_code}")
async def redirect(
    short_code: str,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> RedirectResponse:
    redirect_service = RedirectService(db, client)
    redirect_response = await redirect_service.redirect(short_code)
    return redirect_response
