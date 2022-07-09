import json


class RedisClientWrapper:
    def __init__(self, redis):
        super().__init__()
        self._redis = redis

    async def get_cached_data(self, key):
        data = await self._redis.get(key)
        if data is not None:
            data = json.loads(data)

        return data

    async def cache_data(self, key, data, timeout):
        data = json.dumps(data)
        await self._redis.set(key, data, ex=timeout)
