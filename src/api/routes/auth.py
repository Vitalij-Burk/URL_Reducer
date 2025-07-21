from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from infrastructure.storages.db.session import get_db
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.auth import AuthService
from src.core.domain.schemas.pydantic.auth import Token
from src.infrastructure.storages.cache.client import get_redis_client


auth_router = APIRouter()


@auth_router.post("/token", response_model=Token)
async def login_by_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> Token:
    auth_service = AuthService(db, client)
    token = await auth_service.login_by_access_token(form_data)
    return token
