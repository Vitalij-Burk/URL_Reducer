from redis.asyncio import Redis


class UserDAL:
    def __init__(self, client: Redis):
        self.client = client

    async def create(self, key: str, user):
        return await self.client.set(key, user, 60)

    async def get(self, key: str):
        return await self.client.get(key)

    async def delete(self, key: str):
        return await self.client.delete(key)
