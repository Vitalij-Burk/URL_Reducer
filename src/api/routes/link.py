from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from infrastructure.storages.cache.client import get_redis_client
from infrastructure.storages.db.session import get_db
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.link import LinkService
from src.core.domain.schemas.pydantic.link import CreateLink
from src.core.domain.schemas.pydantic.link import DeletedLinkResponse
from src.core.domain.schemas.pydantic.link import LinkResponse
from src.core.domain.schemas.pydantic.link import UpdateLinkRequest
from src.core.domain.schemas.pydantic.user import UserResponse
from src.infrastructure.auth.authenticator import get_current_user_from_token


link_router = APIRouter()


logger = getLogger(__name__)


@link_router.post("/", response_model=LinkResponse)
async def create_link(
    body: CreateLink,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> LinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.create_link(body, current_user)
    return link


@link_router.get("/{link_id}", response_model=LinkResponse)
async def get_link_by_id(
    link_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> LinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.get_link_by_id(link_id, current_user)
    return link


@link_router.patch("/{link_id}", response_model=LinkResponse)
async def update_link(
    link_id: UUID,
    body: UpdateLinkRequest,
    client: Redis = Depends(get_redis_client),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> LinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.update_link(link_id, body, current_user)
    return link


@link_router.delete("/{link_id}", response_model=DeletedLinkResponse)
async def delete_link(
    link_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> DeletedLinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.delete_link(link_id, current_user)
    return link
