import json
import os
from shared_services.redis_client import r

redis_queue = os.getenv("REDIS_QUEUE", "jobs")

def push_job(job):
    r.rpush(redis_queue, json.dumps(job))

def get_all_jobs():
    return r.lrange(redis_queue, 0, -1)
