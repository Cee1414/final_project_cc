# shared_services/redis/queue.py
import json
import os
from shared_services.redis.client import r  # ensure client.py sets decode_responses=True

QUEUE_KEY = os.getenv("REDIS_QUEUE", "jobs_queue")
r.delete(QUEUE_KEY)

def push_job(job: dict) -> None:
    # FIFO: push right
    r.rpush(QUEUE_KEY, json.dumps(job))

def pop_job(block: bool = False, timeout: int = 0):
    """
    Pop one job JSON string.
    - Non-blocking: returns None if empty.
    - Blocking: waits up to `timeout` seconds.
    """
    if block:
        res = r.brpop(QUEUE_KEY, timeout=timeout)  # (key, value) or None
        return res[1] if res else None
    return r.lpop(QUEUE_KEY)

def get_all_jobs():
    return r.lrange(QUEUE_KEY, 0, -1)
