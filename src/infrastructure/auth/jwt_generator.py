from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional

from jose import jwt

from src.core.domain.settings import Config
from src.core.interfaces.crypto_provider import ICryptoProvider


class JWTGenerator(ICryptoProvider):
    @classmethod
    def create(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            Config.ACCESS_TOKEN_SECRET_KEY,
            algorithm=Config.ACCESS_TOKEN_ALGORITHM,
        )
        return encoded_jwt

    @classmethod
    def verify(cls, data: dict, expires_delta: timedelta | None = None) -> str: ...
