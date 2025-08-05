from datetime import timedelta

from src.auth.core.domain.exceptions.auth import InvalidCredentials
from src.auth.core.domain.schemas.out.auth import AccessToken
from src.auth.core.interfaces.authenticator import IAuthenticator
from src.auth.core.interfaces.crypto_provider import ICryptoProvider
from src.core.domain.settings import Config


class LoginByAccessTokenUseCase:
    def __init__(self, authenticator: IAuthenticator, crypto_provider: ICryptoProvider):
        self.authenticator = authenticator
        self.crypto_provider = crypto_provider

    async def execute(self, email: str, password: str) -> AccessToken:
        user = await self.authenticator.authenticate_user(email, password)
        if not user:
            raise InvalidCredentials
        refresh_token = self.crypto_provider.create(
            data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
            secret_key=Config.REFRESH_TOKEN_SECRET_KEY,
            algorithm=Config.REFRESH_TOKEN_ALGORITHM,
            expires_delta=timedelta(minutes=Config.REFRESH_TOKEN_EXPIRE_MINUTES),
        )
        access_token = self.crypto_provider.create(
            data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
            secret_key=Config.ACCESS_TOKEN_SECRET_KEY,
            algorithm=Config.REFRESH_TOKEN_ALGORITHM,
            expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return AccessToken(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )
