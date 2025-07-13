from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from infrastructure.storages.db.session import get_db
from jose import jwt
from jose import JWTError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.domain.schemas.safe.user import UserResponse
from src.core.domain.settings import Config
from src.core.utils.serializers.from_pydantic.user import pydantic_inner_user_to_safe
from src.infrastructure.auth.password_hasher import Password
from src.infrastructure.storages.cache.client import get_redis_client
from src.infrastructure.storages.manager.user_repository_manager import (
    UserRepositoryManager,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Authentication:
    def __init__(self, session: AsyncSession, client: Redis):
        self.session = session
        self.client = client
        self.user_manager = UserRepositoryManager(session, client)

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_manager.get_by_email(email)
        if not user:
            return
        if not Password.verify_password(password, user.hashed_password):
            return
        return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )
    user_manager = UserRepositoryManager(session, client)
    try:
        payload = jwt.decode(
            token,
            Config.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[Config.ACCESS_TOKEN_ALGORITHM],
        )
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    user = await user_manager.get_by_email(email)
    if not user:
        raise credentials_exception
    return pydantic_inner_user_to_safe(user)
