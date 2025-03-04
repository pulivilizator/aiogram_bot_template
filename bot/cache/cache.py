from __future__ import annotations

import asyncio
from typing import Self

from redis.asyncio import Redis

from bot.core.enums import CacheLoadModules

from .base import BaseUserCache
from .models import Settings


class UserCache(BaseUserCache):
    def __init__(self, user_id: int, redis: Redis[str]) -> None:
        self.user_id = user_id
        self.redis = redis
        self.settings = Settings(self)
        self.ex_time = 60 * 60 * 6

    async def load(self, load_modules: list[CacheLoadModules] | None = None) -> Self:
        if load_modules is None:
            load_modules = list(CacheLoadModules)
        tasks = [getattr(self, module).load() for module in load_modules]
        await asyncio.gather(*tasks)
        return self

    def find(self, key: str) -> str | int | None:
        for attr in self.__dict__.values():
            data = getattr(attr, "_data", None)
            if isinstance(data, dict) and key in data:
                return data.get(key)
        return None
