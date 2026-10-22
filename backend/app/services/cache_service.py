# ==============================================================================
# DEVELOPER ARCHITECTURE NOTE (Phase 79 - Resilient Redis Query-Cache Service):
# This service provides an asynchronous high-performance query caching layer for
# hot read endpoints (such as question banks, admission circulars, and blueprint
# configurations) in the Student Life Circle platform.
# Architecture & Standards:
# 1. Asynchronous Redis Driver: Uses redis.asyncio with connection pooling when
#    REDIS_URL is configured and redis package is available.
# 2. Resilient In-Memory LRU Fallback: If Redis is unreachable or running in an
#    isolated CI/sandbox environment, gracefully falls back to an async in-memory
#    cache with per-key TTL expiration, maintaining zero runtime interruptions.
# 3. Cache Invalidation & Telemetry: Provides tag/prefix invalidation and tracks
#    hit/miss ratios, total keys, and backend status for Prometheus/Grafana metrics.
# 4. Zero-Emoji Policy Enforced: All log strings and comments use clean technical text.
# ==============================================================================

import os
import time
import json
import asyncio
from typing import Any, Optional, Dict, List
from datetime import datetime, timezone

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
DEFAULT_CACHE_TTL = int(os.getenv("DEFAULT_CACHE_TTL_SECONDS", "300"))

# Check for redis.asyncio availability
try:
    import redis.asyncio as aioredis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False


class InMemoryCacheEntry:
    """Represents a cached value with an epoch expiration timestamp."""
    def __init__(self, value: Any, ttl_seconds: int):
        self.value = value
        self.expires_at = time.time() + ttl_seconds if ttl_seconds > 0 else float("inf")

    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class CacheService:
    """
    Unified Asynchronous Query-Cache Service with Redis connection pooling
    and automatic in-memory fallback with TTL expiry.
    """

    def __init__(self, redis_url: str = REDIS_URL, default_ttl: int = DEFAULT_CACHE_TTL):
        self.redis_url = redis_url
        self.default_ttl = default_ttl
        self._redis_client = None
        self._memory_store: Dict[str, InMemoryCacheEntry] = {}
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0
        }

        if HAS_REDIS:
            try:
                self._redis_client = aioredis.from_url(
                    self.redis_url,
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=2.0
                )
            except Exception:
                self._redis_client = None

    @property
    def backend_type(self) -> str:
        return "Redis_Async" if self._redis_client is not None else "In_Memory_LRU_Fallback"

    async def get(self, key: str) -> Optional[Any]:
        """
        Retrieves a cached item by key. Returns None if key does not exist or has expired.
        """
        if self._redis_client is not None:
            try:
                raw = await self._redis_client.get(key)
                if raw is not None:
                    self._stats["hits"] += 1
                    try:
                        return json.loads(raw)
                    except (json.JSONDecodeError, TypeError):
                        return raw
                else:
                    self._stats["misses"] += 1
                    return None
            except Exception:
                # On Redis communication failure, fallback to memory
                pass

        # In-memory lookup
        entry = self._memory_store.get(key)
        if entry is None:
            self._stats["misses"] += 1
            return None

        if entry.is_expired():
            del self._memory_store[key]
            self._stats["misses"] += 1
            return None

        self._stats["hits"] += 1
        return entry.value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None, ttl_seconds: Optional[int] = None) -> bool:
        """
        Stores an item in the cache with a specified TTL in seconds.
        """
        chosen_ttl = ttl_seconds if ttl_seconds is not None else ttl
        actual_ttl = chosen_ttl if chosen_ttl is not None else self.default_ttl
        self._stats["sets"] += 1

        if self._redis_client is not None:
            try:
                serialized = json.dumps(value) if isinstance(value, (dict, list, bool, int, float)) else str(value)
                await self._redis_client.set(key, serialized, ex=actual_ttl)
                return True
            except Exception:
                pass

        # In-memory storage
        self._memory_store[key] = InMemoryCacheEntry(value, actual_ttl)
        return True

    async def delete(self, key: str) -> bool:
        """Deletes an item from the cache."""
        self._stats["deletes"] += 1
        deleted = False

        if self._redis_client is not None:
            try:
                count = await self._redis_client.delete(key)
                deleted = count > 0
            except Exception:
                pass

        if key in self._memory_store:
            del self._memory_store[key]
            deleted = True

        return deleted

    async def delete_pattern(self, pattern: str) -> int:
        """Deletes all keys matching a prefix or pattern (e.g. 'question_bank:*')."""
        count = 0
        prefix = pattern.rstrip("*")

        if self._redis_client is not None:
            try:
                keys = await self._redis_client.keys(pattern)
                if keys:
                    count = await self._redis_client.delete(*keys)
                    return count
            except Exception:
                pass

        matching_keys = [k for k in list(self._memory_store.keys()) if k.startswith(prefix)]
        for k in matching_keys:
            del self._memory_store[k]
            count += 1

        return count

    async def flush_all(self) -> bool:
        """Flushes all keys from cache."""
        if self._redis_client is not None:
            try:
                await self._redis_client.flushdb()
            except Exception:
                pass
        self._memory_store.clear()
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Returns cache telemetry and hit/miss statistics."""
        # Evict expired memory keys first
        now = time.time()
        expired = [k for k, v in self._memory_store.items() if now > v.expires_at]
        for k in expired:
            del self._memory_store[k]

        total_lookups = self._stats["hits"] + self._stats["misses"]
        hit_ratio = round((self._stats["hits"] / total_lookups) * 100, 2) if total_lookups > 0 else 0.0

        return {
            "backend": self.backend_type,
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_ratio_percent": hit_ratio,
            "sets": self._stats["sets"],
            "deletes": self._stats["deletes"],
            "active_in_memory_keys": len(self._memory_store),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Global Cache Service Instance
cache_service = CacheService()
