from decouple import config
from datetime import datetime, timedelta

import aioredis, json


class Cache:
    REDIS_URL = f"http://localhost:{config('REDIS_PORT')}"
    REDIS_PASSWORD = config("REDIS_PASSWORD")
    REDIS_USER = "user"
    EXPIRY_DURATION = timedelta(minutes=30)

    @classmethod
    async def _get_redis_instance(cls):
        return await aioredis.from_url(
            cls.REDIS_URL, username=cls.REDIS_USER, password=cls.REDIS_PASSWORD
        )

    @classmethod
    def __datetime_parser(cls, dct: dict):
        for k, v in dct.items():
            if isinstance(v, str) and v.endswith("+00:00"):
                try:
                    dct[k] = datetime.datetime.fromisoformat(v)
                except:
                    pass
        return dct

    @classmethod
    def __serialize_dates(cls, v):
        return v.isoformat() if isinstance(v, datetime) else v

    @classmethod
    async def get(cls, key: str):
        redis = await cls._get_redis_instance()
        current_hour_stats = await redis.get(key)

        if current_hour_stats:
            return json.loads(current_hour_stats, object_hook=cls.__datetime_parser)

    @classmethod
    async def set(cls, data, key: str):
        redis = await cls._get_redis_instance()
        await redis.set(
            key,
            json.dumps(data, default=cls.__serialize_dates),
            ex=cls.EXPIRY_DURATION,
        )

    @classmethod
    async def rmeove(cls, key: str):
        redis = await cls._get_redis_instance()
        await redis.delete(key)
