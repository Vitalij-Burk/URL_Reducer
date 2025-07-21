from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from infrastructure.storages.db.session import get_db
from jose import jwt
from jose import JWTError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.domain.exceptions.auth import InvalidCredentials
from src.core.domain.schemas.pydantic.user import UserResponse
from src.core.domain.settings import Config
from src.core.interfaces.authenticator import IAuthenticator
from src.core.utils.serializers.from_inner.user import serialize_to_safe_user
from src.infrastructure.auth.password_hasher import PasswordHasher
from src.infrastructure.storages.cache.client import get_redis_client
from src.infrastructure.storages.manager.user_repository_manager import (
    UserRepositoryManager,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Authenticator(IAuthenticator):
    def __init__(self, session: AsyncSession, client: Redis):
        self.session = session
        self.client = client
        self.user_manager = UserRepositoryManager(session, client)
        self.hasher = PasswordHasher()

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_manager.get_by_email(email)
        if not user:
            return
        if not self.hasher.verify(password, user.hashed_password):
            return
        return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> UserResponse:
    user_manager = UserRepositoryManager(session, client)
    try:
        payload = jwt.decode(
            token,
            Config.ACCESS_TOKEN_SECRET_KEY,
            algorithms=[Config.ACCESS_TOKEN_ALGORITHM],
        )
        email: str = payload.get("sub")
    except JWTError:
        raise InvalidCredentials
    user = await user_manager.get_by_email(email)
    if not user:
        raise InvalidCredentials
    return serialize_to_safe_user(user)
