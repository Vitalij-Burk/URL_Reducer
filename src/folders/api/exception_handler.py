from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.domain.exceptions.base import AppError
from src.core.domain.logger import app_logger
from src.folders.core.domain.exceptions.folder import FolderAlreadyExists
from src.folders.core.domain.exceptions.folder import FolderForbidden
from src.folders.core.domain.exceptions.folder import FolderLimitExceeded
from src.folders.core.domain.exceptions.folder import FolderNesting
from src.folders.core.domain.exceptions.folder import FolderNotFound
from src.folders.core.domain.exceptions.folder import FolderParams


async def folder_exception_handler(request: Request, exc: AppError):
    if isinstance(exc, FolderForbidden):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=403,
            content={
                "detail": f"Forbidden. User '{exc.current_id}' has no access to folder '{exc.req_id}'."
            },
        )
    if isinstance(exc, FolderNesting):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=409,
            content={
                "detail": f"Nesting error. folder '{exc.folder_id}' can not be moved to '{exc.move_id}'."
            },
        )
    if isinstance(exc, FolderLimitExceeded):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=429,
            content={"detail": f"Folder '{exc.exceeded}' limit exceeded."},
        )
    if isinstance(exc, FolderNotFound):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=404, content={"detail": f"Folder '{exc.id}' not found."}
        )
    if isinstance(exc, FolderAlreadyExists):
        app_logger.info(exc)
        return JSONResponse(
            status_code=409,
            content={"detail": f"Folder '{exc.id}' already exists."},
        )
    if isinstance(exc, FolderParams):
        app_logger.info(exc)
        return JSONResponse(
            status_code=422,
            content={"detail": f"Folder with current params could not be validated."},
        )
    app_logger.error("Unexpected exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error."},
    )
