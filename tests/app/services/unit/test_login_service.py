from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.app.services.auth import AuthService
from src.infrastructure.auth.jwt import AccessToken


@pytest.mark.asyncio
async def test_login_by_access_token_success(fake_users):
    current_user = fake_users.inner
    service = AuthService(db=AsyncMock(), client=AsyncMock())
    service.authentication.authenticate_user = AsyncMock(return_value=current_user)

    form_data = OAuth2PasswordRequestForm(
        username="tester@mail.com", password="password"
    )

    with patch.object(AccessToken, "create_access_token", return_value="fake_token"):
        result = await service.login_by_access_token(form_data)

    service.authentication.authenticate_user.assert_awaited_once_with(
        "tester@mail.com", "password"
    )
    assert result == {"access_token": "fake_token", "token_type": "bearer"}


@pytest.mark.asyncio
async def test_login_by_access_token_unauthorized(fake_users):
    service = AuthService(db=AsyncMock(), client=AsyncMock())
    service.authentication.authenticate_user = AsyncMock(return_value=None)

    form_data = OAuth2PasswordRequestForm(
        username="tester@mail.com", password="password"
    )

    with patch.object(AccessToken, "create_access_token", return_value="fake_token"):
        with pytest.raises(HTTPException) as exc:
            await service.login_by_access_token(form_data)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Incorrect email or password."
