import redis
from .config import settings

redis_client = redis.Redis(
    host=settings.redis_hostname,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=True
)