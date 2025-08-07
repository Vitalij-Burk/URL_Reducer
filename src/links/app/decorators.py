from functools import wraps
from uuid import UUID

from src.core.domain.logger import app_logger
from src.links.core.domain.schemas.out.link import MoveLinkRequest


def check_user_ownership_by_link_id(func):
    @wraps(func)
    async def wrapper(self, *args, link_id: UUID, current_user_id: UUID, **kwargs):
        if not link_id or not current_user_id:
            app_logger.error("Could not validate named kwargs in decorator")
            raise ValueError("Couldn't extract link_id or current_user_id.")

        await self.guard.check_user_ownership_by_link_id(link_id, current_user_id)

        return await func(
            self, *args, link_id=link_id, current_user_id=current_user_id, **kwargs
        )

    return wrapper


def check_user_ownership_by_folder_id(func):
    @wraps(func)
    async def wrapper(
        self, *args, body: MoveLinkRequest, current_user_id: UUID, **kwargs
    ):
        if not body.folder_id or not current_user_id:
            app_logger.error("Could not validate named kwargs in decorator")
            raise ValueError("Couldn't extract folder_id or current_user_id.")

        await self.guard.check_user_ownership_by_folder_id(
            body.folder_id, current_user_id
        )

        return await func(
            self, *args, body=body, current_user_id=current_user_id, **kwargs
        )

    return wrapper
