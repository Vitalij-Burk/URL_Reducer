from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import jwt

from src.auth.core.interfaces.crypto_provider import ICryptoProvider


class JWTGenerator(ICryptoProvider):
    @classmethod
    def create(
        cls, data: dict, secret_key: str, algorithm: str, expires_delta: timedelta
    ) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            secret_key,
            algorithm,
        )
        return encoded_jwt

    @classmethod
    def verify(cls, data: dict, expires_delta: timedelta | None = None) -> str: ...
