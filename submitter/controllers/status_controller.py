from shared_services.redis import queue
from shared_services.dynamodb import job_io
import json

def get_redis_status():
    raw_jobs = queue.get_all_jobs()
    return [json.loads(job_str) for job_str in raw_jobs]

def get_dynamodb_status():
    result = job_io.get_all_jobs()
    return result.get("Items", [])