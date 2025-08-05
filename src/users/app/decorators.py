from functools import wraps
from uuid import UUID

from src.core.domain.logger import app_logger


def check_user_ownership_by_id(func):
    @wraps(func)
    async def wrapper(self, *args, user_id: UUID, current_user_id: UUID, **kwargs):
        if not user_id or not current_user_id:
            app_logger.error("Could not validate named kwargs in decorator")
            raise ValueError("Couldn't extract user_id or current_user_id.")

        await self.guard.check_user_ownership_by_id(user_id, current_user_id)

        return await func(
            self, *args, user_id=user_id, current_user_id=current_user_id, **kwargs
        )

    return wrapper


def check_user_ownership_by_email(func):
    @wraps(func)
    async def wrapper(self, *args, email: str, current_user_email: UUID, **kwargs):
        if not email or not current_user_email:
            app_logger.error("Could not validate named kwargs in decorator")
            raise ValueError("Couldn't extract email or current_user_id.")

        await self.guard.check_user_ownership_by_email(email, current_user_email)

        return await func(
            self, *args, email=email, current_user_email=current_user_email, **kwargs
        )

    return wrapper
