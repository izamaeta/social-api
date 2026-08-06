from fastapi import Request, HTTPException, status
from .redis_client import redis_client

RATE_LIMIT = 5
RATE_LIMIT_WINDOW = 60


def rate_limiter(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    current_count = redis_client.incr(key)

    if current_count == 1:
        redis_client.expire(key, RATE_LIMIT_WINDOW)

    if current_count > RATE_LIMIT:
        ttl = redis_client.ttl(key)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
            headers={"Retry-After": str(ttl)}
        )