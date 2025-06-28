from functools import wraps


class DALDecorators:
    @staticmethod
    def execute_query(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            query = await func(self, *args, **kwargs)
            res = await self.db_session.execute(query)
            await self.db_session.commit()
            return res.scalar_one_or_none()

        return wrapper

    @staticmethod
    def execute_query_all(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            query = await func(self, *args, **kwargs)
            res = await self.db_session.execute(query)
            await self.db_session.commit()
            return res.scalars().all()  # Возвращаем ВСЕ результаты

        return wrapper
