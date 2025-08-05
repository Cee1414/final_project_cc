from datetime import datetime
from zoneinfo import ZoneInfo
import uuid
from shared_services.redis import queue
from shared_services.dynamodb import job_io

def handle_submit(input_data):
    job_id = str(uuid.uuid4())
    time_submitted = datetime.now(ZoneInfo("America/Chicago")).isoformat()
    
    job = {
    "job_id": job_id,
    "input": input_data,
    "status": "queued",
    "submitted_at": time_submitted
    }

    queue.push_job(job)
    job_io.push_job(job)

    return job