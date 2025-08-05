from unittest.mock import AsyncMock
from unittest.mock import Mock

import pytest

from src.auth.core.domain.exceptions.auth import InvalidCredentials
from src.auth.core.domain.schemas.out.auth import AccessToken
from src.auth.core.use_cases.auth.login_by_access_token import LoginByAccessTokenUseCase
from src.users.core.domain.exceptions.user import UserUnauthorized


@pytest.mark.asyncio
async def test_login_by_token_use_case_success(fake_users):
    authenticator = AsyncMock()
    crypto_provider = Mock()
    login_by_token_use_case = LoginByAccessTokenUseCase(authenticator, crypto_provider)

    login_by_token_use_case.authenticator.authenticate_user.return_value = (
        fake_users.inner_resp
    )
    login_by_token_use_case.crypto_provider.create.return_value = (
        "ddadkfdah@#jkfhasD2321"
    )

    result = await login_by_token_use_case.execute(
        fake_users.inner_resp.email, "fgasdsd121"
    )

    authenticator.authenticate_user.assert_awaited_once_with(
        fake_users.inner_resp.email, "fgasdsd121"
    )
    assert result == AccessToken(
        access_token="ddadkfdah@#jkfhasD2321",
        refresh_token="ddadkfdah@#jkfhasD2321",
        token_type="bearer",
    )


@pytest.mark.asyncio
async def test_login_by_token_use_case_invalid_credentials(fake_users):
    authenticator = AsyncMock()
    crypto_provider = Mock()
    login_by_token_use_case = LoginByAccessTokenUseCase(authenticator, crypto_provider)

    login_by_token_use_case.authenticator.authenticate_user.return_value = None

    with pytest.raises(InvalidCredentials):
        await login_by_token_use_case.execute(fake_users.inner_resp.email, "fgasdsd121")
