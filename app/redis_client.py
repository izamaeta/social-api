import redis
import json
from .config import settings

redis_client = redis.Redis(
    host=settings.redis_hostname,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True
)

def get_cached_posts(key: str):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None


def set_cached_posts(key: str, data, ttl: int = 30):
    redis_client.set(key, json.dumps(data), ex=ttl)


def invalidate_posts_cache():
    for key in redis_client.scan_iter("posts_cache:*"):
        redis_client.delete(key)