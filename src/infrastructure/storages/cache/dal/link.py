from redis.asyncio import Redis


class LinkDAL:
    def __init__(self, client: Redis):
        self.client = client

    async def create(self, key: str, link):
        return await self.client.set(key, link, 60)

    async def get(self, key: str):
        return await self.client.get(key)

    async def delete(self, key: str):
        return await self.client.delete(key)
