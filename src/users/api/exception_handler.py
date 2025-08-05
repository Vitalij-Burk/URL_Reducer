from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.domain.exceptions.base import AppError
from src.core.domain.logger import app_logger
from src.users.core.domain.exceptions.user import UserAlreadyExists
from src.users.core.domain.exceptions.user import UserForbidden
from src.users.core.domain.exceptions.user import UserNotFound
from src.users.core.domain.exceptions.user import UserUnauthorized


async def user_exception_handler(request: Request, exc: AppError):
    if isinstance(exc, UserUnauthorized):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=401, content={"detail": f"User '{exc.id}' unauthorized."}
        )
    if isinstance(exc, UserForbidden):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=403,
            content={
                "detail": f"Forbidden. User '{exc.current_id}' has no access to user '{exc.req_id}'."
            },
        )
    if isinstance(exc, UserNotFound):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=404, content={"detail": f"User '{exc.id}' not found."}
        )
    if isinstance(exc, UserAlreadyExists):
        app_logger.info(exc)
        return JSONResponse(
            status_code=409,
            content={"detail": f"User '{exc.id}' already exists."},
        )
