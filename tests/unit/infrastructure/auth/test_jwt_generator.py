from datetime import timedelta

from src.core.domain.settings import Config
from src.infrastructure.auth.jwt_generator import JWTGenerator


def test_create_access_token_success_with_expires(fake_users):
    access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTGenerator.create(
        data={"sub": fake_users.safe_resp.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    assert type(access_token) is str


def test_create_access_token_success_without_expires(fake_users):
    access_token = JWTGenerator.create(
        data={"sub": fake_users.safe_resp.email, "other_custom_data": [1, 2, 3, 4]},
    )
    assert type(access_token) is str
