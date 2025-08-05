from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.infrastructure.auth.authenticator import get_current_user_from_token
from src.folders.app.services.folder import FolderService
from src.folders.core.domain.schemas.out.folder import CreateFolderRequest
from src.folders.core.domain.schemas.out.folder import DeletedFolderResponse
from src.folders.core.domain.schemas.out.folder import FolderResponse
from src.folders.core.domain.schemas.out.folder import MoveFolderRequest
from src.folders.core.domain.schemas.out.folder import UpdateFolderRequest
from src.folders.infrastructure.storages.cache.base.client import get_redis_client
from src.folders.infrastructure.storages.db.base.session import get_db
from src.users.core.domain.schemas.out.user import UserResponse


folder_router = APIRouter()


logger = getLogger(__name__)


@folder_router.post("/", response_model=FolderResponse)
async def create_folder(
    body: CreateFolderRequest,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> FolderResponse:
    folder_service = FolderService(db, client)
    folder = await folder_service.create_folder(
        body=body, current_user_id=current_user.user_id
    )
    return folder


@folder_router.get("/{folder_id}", response_model=FolderResponse)
async def get_folder_by_id(
    folder_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> FolderResponse:
    folder_service = FolderService(db, client)
    folder = await folder_service.get_folder_by_id(
        folder_id=folder_id, current_user_id=current_user.user_id
    )
    return folder


@folder_router.patch("/upd/{folder_id}", response_model=FolderResponse)
async def update_folder(
    folder_id: UUID,
    body: UpdateFolderRequest,
    client: Redis = Depends(get_redis_client),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> FolderResponse:
    folder_service = FolderService(db, client)
    folder = await folder_service.update_folder(
        folder_id=folder_id, body=body, current_user_id=current_user.user_id
    )
    return folder


@folder_router.patch("/mv/{folder_id}", response_model=FolderResponse)
async def move_folder(
    folder_id: UUID,
    body: MoveFolderRequest,
    client: Redis = Depends(get_redis_client),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> FolderResponse:
    folder_service = FolderService(db, client)
    folder = await folder_service.move_folder(
        folder_id=folder_id, body=body, current_user_id=current_user.user_id
    )
    return folder


@folder_router.delete("/{folder_id}", response_model=DeletedFolderResponse)
async def delete_folder(
    folder_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> DeletedFolderResponse:
    folder_service = FolderService(db, client)
    folder = await folder_service.delete_folder(
        folder_id=folder_id, current_user_id=current_user.user_id
    )
    return folder
