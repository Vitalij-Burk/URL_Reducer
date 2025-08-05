from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.core.use_cases.auth.login_by_access_token import LoginByAccessTokenUseCase
from src.auth.core.use_cases.auth.login_by_refresh_token import (
    LoginByRefreshTokenUseCase,
)
from src.auth.infrastructure.auth.authenticator import Authenticator
from src.auth.infrastructure.auth.jwt_generator import JWTGenerator
from src.core.domain.logger import app_logger
from src.core.domain.settings import Config


class AuthService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.authenticator = Authenticator(db, client)
        self.jwt_generator = JWTGenerator()
        self.login_by_access_token_use_case = LoginByAccessTokenUseCase(
            self.authenticator, self.jwt_generator
        )
        self.login_by_refresh_token_use_case = LoginByRefreshTokenUseCase(
            self.authenticator, self.jwt_generator
        )

    async def login_by_access_token(self, form_data: OAuth2PasswordRequestForm):
        token = await self.login_by_access_token_use_case.execute(
            form_data.username, form_data.password
        )
        await self.client.set(
            f"refresh:{token.refresh_token}",
            token.refresh_token,
            ex=60 * Config.REFRESH_TOKEN_EXPIRE_MINUTES,
        )
        app_logger.info(token.refresh_token)
        return token

    async def login_by_refresh_token(self, refresh_token: str):
        token = await self.login_by_refresh_token_use_case.execute(refresh_token)
        await self.client.delete(f"refresh:{refresh_token}")
        await self.client.set(
            f"refresh:{token.refresh_token}",
            token.refresh_token,
            ex=60 * Config.REFRESH_TOKEN_EXPIRE_MINUTES,
        )
        app_logger.info(token.refresh_token)
        return token
