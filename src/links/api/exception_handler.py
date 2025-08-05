from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.domain.exceptions.base import AppError
from src.core.domain.logger import app_logger
from src.links.core.domain.exceptions.link import LinkAlreadyExists
from src.links.core.domain.exceptions.link import LinkForbidden
from src.links.core.domain.exceptions.link import LinkLimitExceeded
from src.links.core.domain.exceptions.link import LinkNotFound


async def link_exception_handler(request: Request, exc: AppError):
    if isinstance(exc, LinkForbidden):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=403,
            content={
                "detail": f"Forbidden. User '{exc.current_id}' has no access to link '{exc.req_id}'."
            },
        )
    if isinstance(exc, LinkLimitExceeded):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=429,
            content={"detail": f"Link '{exc.exceeded}' limit exceeded."},
        )
    if isinstance(exc, LinkNotFound):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=404, content={"detail": f"Link '{exc.id}' not found."}
        )
    if isinstance(exc, LinkAlreadyExists):
        app_logger.info(exc)
        return JSONResponse(
            status_code=409,
            content={"detail": f"Link '{exc.id}' already exists."},
        )
    app_logger.error("Unexpected exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error."},
    )
