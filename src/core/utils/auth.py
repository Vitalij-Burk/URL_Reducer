from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional

from core.settings import Config
from jose import jwt


class AccessToken:
    @staticmethod
    def create_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
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
