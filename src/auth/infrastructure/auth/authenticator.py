from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.core.domain.exceptions.auth import InvalidCredentials
from src.auth.core.interfaces.authenticator import IAuthenticator
from src.auth.infrastructure.auth.password_hasher import PasswordHasher
from src.core.domain.settings import Config
from src.users.core.domain.schemas.out.user import UserResponse
from src.users.core.utils.serializers.from_inner import serialize_to_safe_user
from src.users.infrastructure.storages.cache.base.client import get_redis_client
from src.users.infrastructure.storages.db.base.session import get_db
from src.users.infrastructure.storages.user_repository_manager import (
    UserRepositoryManager,
)


oauth2_scheme_access = OAuth2PasswordBearer(tokenUrl="/auth/token")


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
    access_token: str = Depends(oauth2_scheme_access),
    session: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
) -> UserResponse:
    user_manager = UserRepositoryManager(session, client)
    try:
        payload = jwt.decode(
            access_token,
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
