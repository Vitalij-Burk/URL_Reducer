from datetime import timedelta

from src.auth.infrastructure.auth.jwt_generator import JWTGenerator
from src.core.domain.settings import Config


def test_create_access_token_success_with_expires(fake_users):
    access_token = JWTGenerator.create(
        data={"sub": fake_users.safe_resp.email, "other_custom_data": [1, 2, 3, 4]},
        secret_key=Config.TEST_ACCESS_TOKEN_SECRET_KEY,
        algorithm=Config.TEST_ACCESS_TOKEN_ALGORITHM,
        expires_delta=timedelta(minutes=Config.TEST_ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    assert type(access_token) is str
