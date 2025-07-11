from datetime import timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.domain.settings import Config
from src.infrastructure.auth.auth import Authentication
from src.infrastructure.auth.jwt import AccessToken


class LoginService:
    def __init__(self, db: AsyncSession, client: Redis):
        self.db = db
        self.client = client
        self.authentication = Authentication(db, client)

    async def login_by_access_token(self, form_data: OAuth2PasswordRequestForm):
        user = await self.authentication.authenticate_user(
            form_data.username, form_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password.",
            )
        access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AccessToken.create_access_token(
            data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
