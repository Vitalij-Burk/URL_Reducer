from functools import wraps
from uuid import UUID

from src.core.domain.schemas.pydantic.user import UserResponse


def check_user_ownership_by_id(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        user_id = kwargs.get("user_id")
        current_user = kwargs.get("current_user")

        for arg in args:
            if isinstance(arg, UUID) and user_id is None:
                user_id = arg
            elif isinstance(arg, UserResponse) and current_user is None:
                current_user = arg

        if not user_id or not current_user:
            raise ValueError("Couldn't extract user_id or current_user.")

        await self.guard.check_user_ownership_by_id(user_id, current_user)

        return await func(self, *args, **kwargs)

    return wrapper


def check_user_ownership_by_email(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        email = kwargs.get("email")
        current_user = kwargs.get("current_user")

        for arg in args:
            if isinstance(arg, str) and email is None:
                email = arg
            elif isinstance(arg, UserResponse) and current_user is None:
                current_user = arg

        if not email or not current_user:
            raise ValueError("Couldn't extract email or current_user.")

        await self.guard.check_user_ownership_by_email(email, current_user)

        return await func(self, *args, **kwargs)

    return wrapper
