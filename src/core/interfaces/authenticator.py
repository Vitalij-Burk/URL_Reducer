from abc import ABC


class IAuthenticator(ABC):
    async def authenticate_user(self, email: str, password: str): ...
