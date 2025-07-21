from datetime import timedelta

from src.core.domain.exceptions.user import UserUnauthorized
from src.core.domain.settings import Config
from src.core.interfaces.authenticator import IAuthenticator
from src.core.interfaces.crypto_provider import ICryptoProvider


class LoginByAccessTokenUseCase:
    def __init__(self, authenticator: IAuthenticator, crypto_provider: ICryptoProvider):
        self.authenticator = authenticator
        self.crypto_provider = crypto_provider

    async def execute(self, email: str, password: str) -> dict:
        user = await self.authenticator.authenticate_user(email, password)
        if not user:
            raise UserUnauthorized(email)
        access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.crypto_provider.create(
            data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
