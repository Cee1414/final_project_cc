# shared_services/redis/client.py
import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

# decode_responses=True gives you str instead of bytes
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def ping() -> bool:
    try:
        return r.ping()
    except Exception:
        return False
