from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.infrastructure.auth.authenticator import get_current_user_from_token
from src.links.app.services.link import LinkService
from src.links.core.domain.schemas.out.link import CreateLinkRequest
from src.links.core.domain.schemas.out.link import DeletedLinkResponse
from src.links.core.domain.schemas.out.link import LinkResponse
from src.links.core.domain.schemas.out.link import MoveLinkRequest
from src.links.core.domain.schemas.out.link import UpdateLinkRequest
from src.links.infrastructure.storages.cache.base.client import get_redis_client
from src.links.infrastructure.storages.db.base.session import get_db
from src.users.core.domain.schemas.out.user import UserResponse


link_router = APIRouter()


logger = getLogger(__name__)


@link_router.post("/", response_model=LinkResponse)
async def create_link(
    body: CreateLinkRequest,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> LinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.create_link(
        body=body, current_user_id=current_user.user_id
    )
    return link


@link_router.get("/{link_id}", response_model=LinkResponse)
async def get_link_by_id(
    link_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> LinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.get_link_by_id(
        link_id=link_id, current_user_id=current_user.user_id
    )
    return link


@link_router.patch("/upd/{link_id}", response_model=LinkResponse)
async def update_link(
    link_id: UUID,
    body: UpdateLinkRequest,
    client: Redis = Depends(get_redis_client),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> LinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.update_link(
        link_id=link_id, body=body, current_user_id=current_user.user_id
    )
    return link


@link_router.patch("/mv/{link_id}", response_model=LinkResponse)
async def move_link(
    link_id: UUID,
    body: MoveLinkRequest,
    client: Redis = Depends(get_redis_client),
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> LinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.move_link(
        link_id=link_id, body=body, current_user_id=current_user.user_id
    )
    return link


@link_router.delete("/{link_id}", response_model=DeletedLinkResponse)
async def delete_link(
    link_id: UUID,
    db: AsyncSession = Depends(get_db),
    client: Redis = Depends(get_redis_client),
    current_user: UserResponse = Depends(get_current_user_from_token),
) -> DeletedLinkResponse:
    link_service = LinkService(db, client)
    link = await link_service.delete_link(
        link_id=link_id, current_user_id=current_user.user_id
    )
    return link
