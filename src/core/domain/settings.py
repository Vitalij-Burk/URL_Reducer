class Config:
    REAL_DB_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5433/url_reducer"
    )
    TEST_DB_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5434/url_reducer_test"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_TOKEN_SECRET_KEY: str = "key secret"
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    LINK_EXPIRE_MINUTES: int = 60
    REDIS_REAL_PORT: int = 6379
    REDIS_TEST_PORT: int = 6380
