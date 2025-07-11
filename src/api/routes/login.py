from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from infrastructure.storages.db.session import get_db
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.login import LoginService
from src.core.domain.schemas.general.auth import Token
from src.infrastructure.storages.cache.client import get_redis_client


login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_by_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> Token:
    login_service = LoginService(db, client)
    token = await login_service.login_by_access_token(form_data)
    return token
