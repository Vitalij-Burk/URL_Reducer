from logging import getLogger
from uuid import UUID

from api.utils.link.decorators import LinkDecorators
from core.cache.redis.client import redis_client
from core.db.session import get_db
from db.models import User
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from models.schemas.link import CreateLink
from models.schemas.link import DeletedLinkResponse
from models.schemas.link import ShowLink
from models.schemas.link import UpdateLinkRequest
from services.cache_producers.link import LinkCacheProducer
from services.db_producers.link import LinkDBProducer
from services.utils.auth import get_current_user_from_token
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


link_router = APIRouter()


logger = getLogger(__name__)


@link_router.post("/", response_model=ShowLink)
async def create_link(
    body: CreateLink,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowLink:
    try:
        link_db_producer = LinkDBProducer(session=db)
        link_cache_producer = LinkCacheProducer(redis_client=redis_client)
        link = await link_db_producer._create_link(current_user.user_id, body)
        await link_cache_producer._cache_link(link)
        return link
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@link_router.get("/{link_id}", response_model=ShowLink)
@LinkDecorators.check_user_ownership
@LinkDecorators.check_link_available
async def get_link_by_id(
    link_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowLink:
    link_db_producer = LinkDBProducer(session=db)
    link_cache_producer = LinkCacheProducer(redis_client=redis_client)
    if link := await link_cache_producer._get_link_from_cache(link_id):
        return link
    link = await link_db_producer._get_link_by_id(link_id)
    return link


@link_router.patch("/{link_id}", response_model=ShowLink)
@LinkDecorators.check_user_ownership
@LinkDecorators.check_link_available
async def update_link(
    link_id: UUID,
    body: UpdateLinkRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowLink:
    updated_link_params = body.model_dump(exclude_none=True)
    if updated_link_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter should be provided for link update",
        )
    link_db_producer = LinkDBProducer(session=db)
    link_cache_producer = LinkCacheProducer(redis_client=redis_client)
    updated_link = await link_db_producer._update_link(link_id, updated_link_params)
    await link_cache_producer.update_link_in_cache(link_id, updated_link)
    return updated_link


@link_router.delete("/{link_id}", response_model=DeletedLinkResponse)
@LinkDecorators.check_user_ownership
@LinkDecorators.check_link_available
async def delete_link(
    link_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeletedLinkResponse:
    link_db_producer = LinkDBProducer(session=db)
    link_cache_producer = LinkCacheProducer(redis_client=redis_client)
    deleted_link_id = await link_db_producer._delete_link(link_id)
    await link_cache_producer._delete_link_from_cache(link_id)
    return DeletedLinkResponse(deleted_link_id=deleted_link_id)
