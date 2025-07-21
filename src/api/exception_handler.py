from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.core.domain.exceptions.auth import InvalidCredentials
from src.core.domain.exceptions.base import AppError
from src.core.domain.exceptions.link import LinkAlreadyExists
from src.core.domain.exceptions.link import LinkForbidden
from src.core.domain.exceptions.link import LinkLimitExceeded
from src.core.domain.exceptions.link import LinkNotFound
from src.core.domain.exceptions.user import UserAlreadyExists
from src.core.domain.exceptions.user import UserForbidden
from src.core.domain.exceptions.user import UserNotFound
from src.core.domain.exceptions.user import UserUnauthorized
from src.core.domain.logger import logger


async def exception_handler(request: Request, exc: AppError):
    if isinstance(exc, InvalidCredentials):
        logger.warning(exc)
        return JSONResponse(
            status_code=401, content={"detail": "Could not validate credentials."}
        )
    if isinstance(exc, UserUnauthorized):
        logger.warning(exc)
        return JSONResponse(
            status_code=401, content={"detail": f"User '{exc.id}' unauthorized."}
        )
    if isinstance(exc, UserForbidden):
        logger.warning(exc)
        return JSONResponse(
            status_code=403,
            content={
                "detail": f"Forbidden. User '{exc.current_id}' has no access to '{exc.req_id}'."
            },
        )
    if isinstance(exc, UserNotFound):
        logger.warning(exc)
        return JSONResponse(
            status_code=404, content={"detail": f"User '{exc.id}' not found."}
        )
    if isinstance(exc, UserAlreadyExists):
        logger.info(exc)
        return JSONResponse(
            status_code=409,
            content={"detail": f"User '{exc.id}' already exists."},
        )
    if isinstance(exc, LinkForbidden):
        logger.warning(exc)
        return JSONResponse(
            status_code=403,
            content={
                "detail": f"Forbidden. Link '{exc.current_id}' has no access to '{exc.req_id}'."
            },
        )
    if isinstance(exc, LinkLimitExceeded):
        logger.warning(exc)
        return JSONResponse(
            status_code=429,
            content={"detail": f"Link '{exc.exceeded}' limit exceeded."},
        )
    if isinstance(exc, LinkNotFound):
        logger.warning(exc)
        return JSONResponse(
            status_code=404, content={"detail": f"Link '{exc.id}' not found."}
        )
    if isinstance(exc, LinkAlreadyExists):
        logger.info(exc)
        return JSONResponse(
            status_code=409,
            content={"detail": f"Link '{exc.id}' already exists."},
        )
    logger.error("Unexpected exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error."},
    )
