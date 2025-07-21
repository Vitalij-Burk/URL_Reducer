from functools import wraps
from uuid import UUID

from src.core.domain.schemas.pydantic.user import UserResponse


def check_user_ownership_by_link_id(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        link_id = kwargs.get("link_id")
        current_user = kwargs.get("current_user")

        for arg in args:
            if isinstance(arg, UUID) and link_id is None:
                link_id = arg
            elif isinstance(arg, UserResponse) and current_user is None:
                current_user = arg

        if not link_id or not current_user:
            raise ValueError("Couldn't extract link_id or current_user.")

        await self.guard.check_user_ownership_by_link_id(link_id, current_user)

        return await func(self, *args, **kwargs)

    return wrapper
