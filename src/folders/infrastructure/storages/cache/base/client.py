from redis.asyncio import Redis

from src.core.domain.settings import Config


def get_redis_client() -> Redis:
    return Redis(
        host="localhost",
        port=Config.REDIS_REAL_PORT,
        db=0,
        socket_connect_timeout=0.2,
        socket_timeout=0.2,
    )
