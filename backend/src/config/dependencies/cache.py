from decouple import config
from datetime import datetime, timedelta

import aioredis, json


class Cache:
    REDIS_URL = f"http://localhost:{config('REDIS_PORT')}"
    REDIS_PASSWORD = config("REDIS_PASSWORD")
    REDIS_USER = "user"
    EXPIRY_DURATION = timedelta(minutes=30)

    async def _get_redis_instance(self):
        return await aioredis.from_url(
            self.REDIS_URL, username=self.REDIS_USER, password=self.REDIS_PASSWORD
        )

    @classmethod
    def _datetime_parser(dct: dict):
        for k, v in dct.items():
            if isinstance(v, str) and v.endswith("+00:00"):
                try:
                    dct[k] = datetime.datetime.fromisoformat(v)
                except:
                    pass
        return dct

    async def get_cache(self, key: str):
        redis = await self._get_redis_instance()
        current_hour_stats = await redis.get(key)

        if current_hour_stats:
            return json.loads(current_hour_stats, object_hook=self._datetime_parser)

    async def set_cache(self, data, key: str):
        def serialize_dates(v):
            return v.isoformat() if isinstance(v, datetime) else v

        redis = await self._get_redis_instance()
        await redis.set(
            key,
            json.dumps(data, default=serialize_dates),
            ex=self.EXPIRY_DURATION,
        )
