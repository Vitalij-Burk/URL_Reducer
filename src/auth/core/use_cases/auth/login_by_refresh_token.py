from datetime import timedelta

from jose import jwt

from src.auth.core.domain.schemas.out.auth import RefreshToken
from src.auth.core.interfaces.authenticator import IAuthenticator
from src.auth.core.interfaces.crypto_provider import ICryptoProvider
from src.core.domain.settings import Config


class LoginByRefreshTokenUseCase:
    def __init__(self, authenticator: IAuthenticator, crypto_provider: ICryptoProvider):
        self.authenticator = authenticator
        self.crypto_provider = crypto_provider

    async def execute(self, refresh_token: str) -> RefreshToken:
        payload = jwt.decode(
            refresh_token,
            Config.REFRESH_TOKEN_SECRET_KEY,
            algorithms=[Config.ACCESS_TOKEN_ALGORITHM],
        )
        email: str = payload.get("sub")
        access_token = self.crypto_provider.create(
            data={"sub": email, "other_custom_data": [1, 2, 3, 4]},
            secret_key=Config.ACCESS_TOKEN_SECRET_KEY,
            algorithm=Config.ACCESS_TOKEN_ALGORITHM,
            expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        refresh_token = self.crypto_provider.create(
            data={"sub": email, "other_custom_data": [1, 2, 3, 4]},
            secret_key=Config.REFRESH_TOKEN_SECRET_KEY,
            algorithm=Config.REFRESH_TOKEN_ALGORITHM,
            expires_delta=timedelta(minutes=Config.REFRESH_TOKEN_EXPIRE_MINUTES),
        )
        return RefreshToken(
            refresh_token=refresh_token, access_token=access_token, token_type="bearer"
        )
