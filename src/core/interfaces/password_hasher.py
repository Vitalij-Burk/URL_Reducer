from abc import ABC
from abc import abstractmethod


class IPassword(ABC):
    @staticmethod
    @abstractmethod
    def get_password_hash(password: str) -> str: ...

    @staticmethod
    @abstractmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool: ...
