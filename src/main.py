from typing import Callable

import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.auth.api.exception_handler import auth_exception_handler
from src.auth.api.routes.auth import auth_router
from src.core.domain.exceptions.base import AppError
from src.folders.api.exception_handler import folder_exception_handler
from src.folders.api.routes.folder import folder_router
from src.folders.infrastructure.storages.db.base.models import Folder
from src.links.api.exception_handler import link_exception_handler
from src.links.api.routes.link import link_router
from src.links.api.routes.redirect import redirect_router
from src.links.infrastructure.storages.db.base.models import Link
from src.users.api.exception_handler import user_exception_handler
from src.users.api.routes.user import user_router
from src.users.infrastructure.storages.db.base.models import User


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(link_router, prefix="/link", tags=["Link"])
app.include_router(folder_router, prefix="/folder", tags=["Folder"])
app.include_router(redirect_router, tags=["Redirect"])


class AppErrorHandlerFacade:
    def __init__(self):
        self._handlers = {}

    def register(self, module: str, handler: Callable):
        self._handlers[module] = handler

    async def handle(self, request: Request, exc: AppError):
        handler = self._handlers.get(exc.module)
        if handler:
            return await handler(request, exc)
        return JSONResponse(
            status_code=500, content={"detail": f"Unhandled error: {exc.message}"}
        )


error_facade = AppErrorHandlerFacade()
error_facade.register("auth", auth_exception_handler)
error_facade.register("users", user_exception_handler)
error_facade.register("links", link_exception_handler)
error_facade.register("folders", folder_exception_handler)

app.add_exception_handler(AppError, error_facade.handle)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
