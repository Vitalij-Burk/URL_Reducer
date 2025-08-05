class Config:
    BASE_URL: str = "http://localhost:8000"
    REAL_DB_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5433/url_reducer"
    )
    TEST_DB_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5434/url_reducer_test"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    ACCESS_TOKEN_SECRET_KEY: str = "key secret"
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440
    REFRESH_TOKEN_SECRET_KEY: str = "key secret refresh"
    REFRESH_TOKEN_ALGORITHM: str = "HS256"
    TEST_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    TEST_ACCESS_TOKEN_SECRET_KEY: str = "test key secret"
    TEST_ACCESS_TOKEN_ALGORITHM: str = "HS256"
    TEST_REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440
    TEST_REFRESH_TOKEN_SECRET_KEY: str = "test key secret refresh"
    TEST_REFRESH_TOKEN_ALGORITHM: str = "HS256"
    LINK_EXPIRE_MINUTES: int = 60
    REDIS_REAL_PORT: int = 6379
    REDIS_TEST_PORT: int = 6380
    SPEC_CHARS: str = "!@#$%^&*()'/|><?.,}{[]`~-_=+"
    REDIS_DEFAULT_TTL = 30
