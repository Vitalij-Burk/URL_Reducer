from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.use_cases.auth.login_by_token import LoginByAccessTokenUseCase
from src.infrastructure.auth.authenticator import Authenticator
from src.infrastructure.auth.jwt_generator import JWTGenerator


class AuthService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.authenticator = Authenticator(db, client)
        self.jwt_generator = JWTGenerator()
        self.login_by_access_token_use_case = LoginByAccessTokenUseCase(
            self.authenticator, self.jwt_generator
        )

    async def login_by_access_token(self, form_data: OAuth2PasswordRequestForm):
        return await self.login_by_access_token_use_case.execute(
            form_data.username, form_data.password
        )
