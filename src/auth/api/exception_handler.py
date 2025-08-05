from fastapi import Request
from fastapi.responses import JSONResponse

from src.auth.core.domain.exceptions.auth import InvalidCredentials
from src.core.domain.exceptions.base import AppError
from src.core.domain.logger import app_logger


async def auth_exception_handler(request: Request, exc: AppError):
    if isinstance(exc, InvalidCredentials):
        app_logger.warning(exc)
        return JSONResponse(
            status_code=401, content={"detail": "Could not validate credentials."}
        )
