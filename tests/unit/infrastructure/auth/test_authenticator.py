from datetime import datetime
from datetime import timedelta
from datetime import timezone
from unittest.mock import AsyncMock
from unittest.mock import patch

import pytest
from jose import jwt

from src.core.domain.exceptions.auth import InvalidCredentials
from src.core.domain.schemas.pydantic.user import UserResponse
from src.core.domain.settings import Config
from src.infrastructure.auth.authenticator import Authenticator
from src.infrastructure.auth.authenticator import get_current_user_from_token


@pytest.mark.asyncio
async def test_authenticate_user_success(fake_users):
    authenticator = Authenticator(AsyncMock(), AsyncMock())
    authenticator.user_manager.get_by_email = AsyncMock(
        return_value=fake_users.inner_resp
    )

    class PasswordPlug:
        @staticmethod
        def verify(*args, **kwargs):
            return True

    authenticator.hasher = PasswordPlug()

    user = await authenticator.authenticate_user(fake_users.safe_resp.email, "fadasds")

    assert user.email == fake_users.safe_resp.email
    assert user.name == fake_users.safe_resp.name
    assert user.links == fake_users.safe_resp.links


@pytest.mark.asyncio
async def test_authenticate_user_not_found(fake_users):
    authenticator = Authenticator(AsyncMock(), AsyncMock())
    authenticator.user_manager.get_by_email = AsyncMock(return_value=None)

    class PasswordPlug:
        @staticmethod
        def verify(*args, **kwargs):
            return True

    authenticator.hasher = PasswordPlug()

    user = await authenticator.authenticate_user(fake_users.safe_resp.email, "fadasds")

    assert user is None


@pytest.mark.asyncio
async def test_authenticate_user_incorrect_password(fake_users):
    authenticator = Authenticator(AsyncMock(), AsyncMock())
    authenticator.user_manager.get_by_email = AsyncMock(
        return_value=fake_users.inner_resp
    )

    class PasswordPlug:
        @staticmethod
        def verify(*args, **kwargs):
            return False

    authenticator.hasher = PasswordPlug()

    user = await authenticator.authenticate_user(fake_users.safe_resp.email, "fadasds")

    assert user is None


@pytest.mark.asyncio
async def test_get_current_user_from_token_success(fake_users):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "sub": fake_users.safe_resp.email,
        "exp": expire,
    }
    token = jwt.encode(
        payload,
        Config.ACCESS_TOKEN_SECRET_KEY,
        algorithm=Config.ACCESS_TOKEN_ALGORITHM,
    )

    class FakeUserRepository:
        async def get_by_email(self, email_arg):
            assert email_arg == fake_users.safe_resp.email
            return fake_users.safe_resp

    with patch(
        "src.infrastructure.auth.authenticator.UserRepositoryManager",
        lambda *_: FakeUserRepository(),
    ):
        result = await get_current_user_from_token(
            token=token, session=None, client=None
        )
    assert isinstance(result, UserResponse)
    assert result.email == fake_users.safe_resp.email


@pytest.mark.asyncio
async def test_get_current_user_from_token_incorrect_jwt(fake_users):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "sub": fake_users.safe_resp.email,
        "exp": expire,
    }
    token = jwt.encode(
        payload,
        Config.ACCESS_TOKEN_SECRET_KEY,
        algorithm=Config.ACCESS_TOKEN_ALGORITHM,
    )

    class FakeUserRepository:
        async def get_by_email(self, email_arg):
            assert email_arg == fake_users.safe_resp.email
            return None

    with patch(
        "src.infrastructure.auth.authenticator.UserRepositoryManager",
        lambda *_: FakeUserRepository(),
    ):
        with pytest.raises(InvalidCredentials):
            await get_current_user_from_token(token=token, session=None, client=None)


@pytest.mark.asyncio
async def test_get_current_user_from_token_user_not_found(fake_users):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"

    class FakeUserRepository:
        async def get_by_email(self, email_arg):
            assert email_arg == fake_users.safe_resp.email
            return fake_users.safe_resp

    with patch(
        "src.infrastructure.auth.authenticator.UserRepositoryManager",
        lambda *_: FakeUserRepository(),
    ):
        with pytest.raises(InvalidCredentials):
            await get_current_user_from_token(token=token, session=None, client=None)


@pytest.mark.asyncio
async def test_get_current_user_from_token_credentials_exception(fake_users):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30"

    class FakeUserRepository:
        async def get_by_email(self, email_arg):
            assert email_arg == fake_users.safe_resp.email
            return fake_users.safe_resp

    with patch(
        "src.infrastructure.auth.authenticator.UserRepositoryManager",
        lambda *_: FakeUserRepository(),
    ):
        with pytest.raises(InvalidCredentials):
            await get_current_user_from_token(token=token, session=None, client=None)
