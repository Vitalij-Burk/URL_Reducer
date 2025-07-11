from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.services.user import UserService
from src.core.domain.schemas.general.user import UpdateUserRequest
from src.core.domain.schemas.safe.user import CreateUser


@pytest.mark.asyncio
async def test_create_user_success(fake_users):
    mock_db = AsyncMock(spec=AsyncSession)
    mock_redis = AsyncMock(spec=Redis)
    service = UserService(mock_db, mock_redis)

    service.user_manager = AsyncMock()
    service.user_manager.create.return_value = fake_users.inner

    create_user_payload = CreateUser(
        email="test@mail.com", name="tester", password="123456"
    )

    with patch(
        "src.app.services.user.Security.get_password_hash", return_value="hashed_pwd"
    ) as mock_hash, patch(
        "src.app.services.user.pydantic_create_user_to_inner",
        return_value=fake_users.inner,
    ) as mock_serializer, patch(
        "src.app.services.user.pydantic_inner_user_to_safe",
        return_value=fake_users.safe,
    ) as mock_to_safe:

        result = await service.create_user(create_user_payload)

        mock_hash.assert_called_once_with("123456")
        mock_serializer.assert_called_once()
        service.user_manager.create.assert_called_once()
        mock_to_safe.assert_called_once_with(fake_users.inner)

        assert result.email == "test@mail.com"


@pytest.mark.asyncio
async def test_create_user_integrity_error(fake_users):
    mock_db = AsyncMock(spec=AsyncSession)
    mock_redis = AsyncMock(spec=Redis)
    service = UserService(mock_db, mock_redis)

    service.user_manager = AsyncMock()
    service.user_manager.create.side_effect = IntegrityError(
        "duplicate key value violates unique constraint", None, None
    )

    create_user_payload = CreateUser(
        email="test@mail.com", name="tester", password="123456"
    )

    with patch(
        "src.app.services.user.Security.get_password_hash", return_value="hashed_pwd"
    ), patch(
        "src.app.services.user.pydantic_create_user_to_inner",
        return_value=fake_users.inner,
    ), patch(
        "src.app.services.user.pydantic_inner_user_to_safe",
        return_value=fake_users.safe,
    ):

        with pytest.raises(HTTPException) as exc:
            await service.create_user(create_user_payload)

    assert exc.value.status_code == 503
    assert "Database error" in exc.value.detail


@pytest.mark.asyncio
async def test_get_user_by_id_success(fake_users):
    current_user = fake_users.safe
    service = UserService(db=AsyncMock(), client=AsyncMock())
    service.user_manager = AsyncMock()
    service.user_manager.get_by_id.return_value = fake_users.inner
    service.guard = AsyncMock()
    service.guard.check_user_ownership_by_id.return_value = None

    with patch(
        "src.app.services.user.pydantic_inner_user_to_safe",
        return_value=fake_users.safe,
    ):

        result = await service.get_user_by_id(
            user_id=fake_users.safe.user_id, current_user=current_user
        )

        service.user_manager.get_by_id.assert_called_once_with(fake_users.safe.user_id)
        assert result.user_id == fake_users.safe.user_id


@pytest.mark.asyncio
async def test_get_user_by_email_success(fake_users):
    current_user = fake_users.safe
    service = UserService(db=AsyncMock(), client=AsyncMock())
    service.user_manager = AsyncMock()
    service.user_manager.get_by_id.return_value = fake_users.inner
    service.guard = AsyncMock()
    service.guard.check_user_ownership_by_id.return_value = None

    with patch(
        "src.app.services.user.pydantic_inner_user_to_safe",
        return_value=fake_users.safe,
    ):

        result = await service.get_user_by_email(
            email="test@mail.com", current_user=current_user
        )

        service.user_manager.get_by_email.assert_called_once_with("test@mail.com")
        assert result.email == "test@mail.com"


@pytest.mark.asyncio
async def test_update_user_success(fake_users):
    current_user = fake_users.safe
    service = UserService(db=AsyncMock(), client=AsyncMock())
    service.user_manager = AsyncMock()
    service.user_manager.get_by_id.return_value = fake_users.inner
    update_user_params = UpdateUserRequest(name="updated_tester")
    service.guard = AsyncMock()
    service.guard.check_user_ownership_by_id.return_value = None

    with patch(
        "src.app.services.user.pydantic_inner_user_to_safe",
        return_value=fake_users.safe,
    ):

        result = await service.update_user(
            user_id=fake_users.safe.user_id,
            body=update_user_params,
            current_user=current_user,
        )

        service.user_manager.update.assert_called_once_with(
            fake_users.safe.user_id, update_user_params.model_dump()
        )
        assert result.user_id == fake_users.safe.user_id


@pytest.mark.asyncio
async def test_delete_user_success(fake_users):
    current_user = fake_users.safe
    service = UserService(db=AsyncMock(), client=AsyncMock())
    service.user_manager = AsyncMock()
    service.user_manager.get_by_id.return_value = fake_users.inner
    service.guard = AsyncMock()
    service.guard.check_user_ownership_by_id.return_value = None

    with patch(
        "src.app.services.user.pydantic_inner_user_to_safe",
        return_value=fake_users.safe,
    ):

        await service.delete_user(
            user_id=fake_users.safe.user_id, current_user=current_user
        )

        service.user_manager.delete.assert_called_once_with(fake_users.safe.user_id)
