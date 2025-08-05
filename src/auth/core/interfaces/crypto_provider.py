from abc import ABC
from abc import abstractmethod


class ICryptoProvider(ABC):
    @classmethod
    @abstractmethod
    def create(cls, data: str | dict, *args, **kwargs) -> str: ...

    @classmethod
    @abstractmethod
    def verify(cls, data: str, token: str) -> bool | dict: ...
