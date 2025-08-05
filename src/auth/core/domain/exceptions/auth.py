from src.core.domain.exceptions.base import AppError


class InvalidCredentials(AppError):
    def __init__(self):
        super().__init__("auth", "Could not validate credentials")
