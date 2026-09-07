import json
import logging
from typing import Optional, Any
from app.core.config import settings

logger = logging.getLogger("clinixiq.cache")

class CacheManager:
    """
    High-performance cache layer supporting Redis with 
    automatic in-memory fallback for local testing & resilience.
    """
    def __init__(self):
        self._memory_cache = {}
        self._redis = None
        self.is_redis_active = False

    async def connect(self):
        try:
            # Lazy import to keep lightweight
            import redis.asyncio as aioredis
            self._redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
            await self._redis.ping()
            self.is_redis_active = True
            logger.info("Connected to Redis cache at %s", settings.REDIS_URL)
        except Exception as e:
            self.is_redis_active = False
            logger.warning("Redis unavailable (%s). Falling back to in-memory cache layer.", str(e))

    async def disconnect(self):
        if self._redis and self.is_redis_active:
            try:
                await self._redis.close()
            except Exception:
                pass
            self.is_redis_active = False

    async def get(self, key: str) -> Optional[Any]:
        if self.is_redis_active and self._redis:
            try:
                data = await self._redis.get(key)
                return json.loads(data) if data else None
            except Exception:
                pass
        return self._memory_cache.get(key)

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = ttl or settings.CACHE_TTL_SECONDS
        if self.is_redis_active and self._redis:
            try:
                await self._redis.set(key, json.dumps(value), ex=ttl)
                return
            except Exception:
                pass
        self._memory_cache[key] = value

cache_manager = CacheManager()
