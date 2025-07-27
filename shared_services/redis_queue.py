import json
from services.redis_client import r

redis_queue = os.getenv("REDIS_QUEUE", "jobs")

def push_job(job):
    r.rpush(redis_queue, json.dumps(job))

def get_all_jobs():
    return r.lrange("jobs", 0, -1)
