import json
import redis
from .config import settings

redis_client = redis.Redis(
    host=settings.redis_hostname,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2,
)


def get_cached_posts(key: str):
    """Try to read cached posts from Redis.
    If Redis is unreachable, fail silently (fail-open) so the API
    still works, just without the caching speedup."""
    try:
        cached = redis_client.get(key)
    except redis.exceptions.RedisError:
        return None

    if cached:
        return json.loads(cached)
    return None


def set_cached_posts(key: str, data, ttl: int = 30):
    """Try to write posts to the cache. If Redis is unreachable,
    ignore the error — the request already succeeded via Postgres,
    caching is just an optimization, not a requirement."""
    try:
        redis_client.set(key, json.dumps(data), ex=ttl)
    except redis.exceptions.RedisError:
        pass


def invalidate_posts_cache():
    """Try to clear all cached post listings. If Redis is unreachable,
    ignore the error — worst case, stale cache entries expire on
    their own after the TTL window."""
    try:
        for key in redis_client.scan_iter("posts_cache:*"):
            redis_client.delete(key)
    except redis.exceptions.RedisError:
        pass