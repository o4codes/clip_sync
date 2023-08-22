import json
from datetime import datetime, timedelta
from typing import Optional

import aioredis
from decouple import config


class Cache:
    REDIS_HOST = f"redis://{config('REDIS_HOST')}"
    REDIS_PORT = config("REDIS_PORT")
    EXPIRY_DURATION = timedelta(minutes=30)

    @classmethod
    def _get_redis_instance(cls):
        return aioredis.from_url(
            url=f"{cls.REDIS_HOST}:{cls.REDIS_PORT}",
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
    async def get(cls, key: str) -> Optional[dict]:
        redis = cls._get_redis_instance()
        current_hour_stats = await redis.get(key)

        if current_hour_stats:
            return json.loads(current_hour_stats, object_hook=cls.__datetime_parser)

    @classmethod
    async def set(cls, data, key: str):
        redis = cls._get_redis_instance()
        await redis.set(
            key,
            json.dumps(data, default=cls.__serialize_dates),
            ex=cls.EXPIRY_DURATION,
        )

    @classmethod
    async def rmeove(cls, key: str):
        redis = await cls._get_redis_instance()
        await redis.delete(key)
