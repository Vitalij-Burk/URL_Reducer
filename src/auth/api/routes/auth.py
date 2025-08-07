from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.app.services.auth import AuthService
from src.auth.core.domain.schemas.out.auth import AccessToken
from src.auth.core.domain.schemas.out.auth import RefreshToken
from src.users.infrastructure.storages.cache.base.client import get_redis_client
from src.users.infrastructure.storages.db.base.session import get_db


auth_router = APIRouter()


@auth_router.post("/token", response_model=AccessToken | None)
async def login_by_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> AccessToken:
    auth_service = AuthService(db, client)
    token = await auth_service.login_by_access_token(form_data=form_data)
    return token


@auth_router.post("/refresh", response_model=RefreshToken | None)
async def login_by_refresh_token(
    refresh: str,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> RefreshToken:
    auth_service = AuthService(db, client)
    token = await auth_service.login_by_refresh_token(refresh=refresh)
    return token
