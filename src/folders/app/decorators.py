from functools import wraps
from uuid import UUID

from src.core.domain.logger import app_logger
from src.folders.core.domain.exceptions.folder import FolderNesting
from src.folders.core.domain.schemas.inner.folder import FolderResponseInner
from src.folders.core.domain.schemas.out.folder import MoveFolderRequest


def check_user_ownership_by_folder_id(func):
    @wraps(func)
    async def wrapper(self, *args, folder_id: UUID, current_user_id: UUID, **kwargs):
        if not folder_id or not current_user_id:
            app_logger.error("Could not validate named kwargs in decorator")
            raise ValueError("Couldn't extract folder_id or current_user_id.")

        await self.guard.check_user_ownership_by_folder_id(folder_id, current_user_id)

        return await func(
            self, *args, folder_id=folder_id, current_user_id=current_user_id, **kwargs
        )

    return wrapper


def check_user_ownership_by_move_id(func):
    @wraps(func)
    async def wrapper(
        self, *args, body: MoveFolderRequest, current_user_id: UUID, **kwargs
    ):
        if not body.parent_id or not current_user_id:
            app_logger.error("Could not validate named kwargs in decorator")
            raise ValueError("Couldn't extract folder_id or current_user_id.")

        await self.guard.check_user_ownership_by_folder_id(
            body.parent_id, current_user_id
        )

        return await func(
            self, *args, body=body, current_user_id=current_user_id, **kwargs
        )

    return wrapper


def check_is_not_parent_folder(func):
    @wraps(func)
    async def wrapper(self, *args, folder_id: UUID, body: MoveFolderRequest, **kwargs):
        if not folder_id:
            app_logger.error("Could not validate named kwargs in decorator")
            raise ValueError("Couldn't extract folder_id.")

        folder = await self.folder_manager.get_by_id(folder_id)

        all_folder_ids = set()

        async def all_inner_folders(folder: FolderResponseInner):
            all_folder_ids.add(folder.folder_id)
            for child_id in folder.children_ids:
                all_folder_ids.add(child_id)
                child = await self.folder_manager.get_by_id(child_id)
                await all_inner_folders(child)

        await all_inner_folders(folder)

        if body.parent_id in all_folder_ids:
            raise FolderNesting(folder_id, body.parent_id)

        return await func(self, *args, folder_id=folder_id, body=body, **kwargs)

    return wrapper
