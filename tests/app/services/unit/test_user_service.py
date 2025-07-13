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

    service.create_user_use_case = AsyncMock()
    service.create_user_use_case.execute.return_value = fake_users.safe

    create_user_payload = CreateUser(
        email="test@mail.com", name="tester", password="123456"
    )

    with patch("src.app.services.user.logger") as mock_logger:
        result = await service.create_user(create_user_payload)

        service.create_user_use_case.execute.assert_awaited_once_with(
            create_user_payload
        )
        assert result.email == "test@mail.com"
        mock_logger.error.assert_not_called()


@pytest.mark.asyncio
async def test_create_user_integrity_error(fake_users):
    mock_db = AsyncMock(spec=AsyncSession)
    mock_redis = AsyncMock(spec=Redis)
    service = UserService(mock_db, mock_redis)

    service.create_user_use_case = AsyncMock()
    service.create_user_use_case.execute.side_effect = IntegrityError(
        "duplicate key value violates unique constraint", None, None
    )

    create_user_payload = CreateUser(
        email="test@mail.com", name="tester", password="123456"
    )

    with patch("src.app.services.user.logger") as mock_logger:
        with pytest.raises(HTTPException) as exc:
            await service.create_user(create_user_payload)

        service.create_user_use_case.execute.assert_awaited_once_with(
            create_user_payload
        )
        mock_logger.error.assert_called_once()
        assert exc.value.status_code == 503
        assert "Database error" in exc.value.detail


@pytest.mark.asyncio
async def test_get_user_by_id_success(fake_users):
    current_user = fake_users.safe
    service = UserService(db=AsyncMock(), client=AsyncMock())

    service.get_user_by_id_use_case = AsyncMock()
    service.get_user_by_id_use_case.execute.return_value = fake_users.safe

    result = await service.get_user_by_id(
        user_id=fake_users.safe.user_id, current_user=current_user
    )

    service.get_user_by_id_use_case.execute.assert_awaited_once_with(
        fake_users.safe.user_id
    )
    assert result.user_id == fake_users.safe.user_id


@pytest.mark.asyncio
async def test_get_user_by_email_success(fake_users):
    current_user = fake_users.safe
    service = UserService(db=AsyncMock(), client=AsyncMock())

    service.get_user_by_email_use_case = AsyncMock()
    service.get_user_by_email_use_case.execute.return_value = fake_users.safe

    result = await service.get_user_by_email(
        email="test@mail.com", current_user=current_user
    )

    service.get_user_by_email_use_case.execute.assert_awaited_once_with("test@mail.com")
    assert result.email == "test@mail.com"


@pytest.mark.asyncio
async def test_update_user_success(fake_users):
    current_user = fake_users.safe
    service = UserService(db=AsyncMock(), client=AsyncMock())

    service.update_user_use_case = AsyncMock()
    service.update_user_use_case.execute.return_value = fake_users.safe

    update_user_params = UpdateUserRequest(name="updated_tester")

    result = await service.update_user(
        user_id=fake_users.safe.user_id,
        body=update_user_params,
        current_user=current_user,
    )

    service.update_user_use_case.execute.assert_awaited_once_with(
        fake_users.safe.user_id, update_user_params
    )
    assert result.user_id == fake_users.safe.user_id


@pytest.mark.asyncio
async def test_delete_user_success(fake_users):
    current_user = fake_users.safe
    service = UserService(db=AsyncMock(), client=AsyncMock())

    service.delete_user_use_case = AsyncMock()
    service.delete_user_use_case.execute.return_value = fake_users.safe

    await service.delete_user(
        user_id=fake_users.safe.user_id, current_user=current_user
    )

    service.delete_user_use_case.execute.assert_awaited_once_with(
        fake_users.safe.user_id
    )
