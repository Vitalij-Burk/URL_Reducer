from passlib.context import CryptContext

from src.auth.core.interfaces.crypto_provider import ICryptoProvider


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher(ICryptoProvider):
    @classmethod
    def create(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
