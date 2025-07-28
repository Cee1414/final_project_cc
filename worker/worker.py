from shared_services.redis import queue
from shared_services.dynamodb import job_io
import json
import time
import jobs

while True:
    raw_job = queue.pop_job()
    if raw_job:
        job = json.loads(raw_job)
        job_id = job.get("job_id")
        job_io.update_field(job_id, "status", "in-progress")
        print(f"starting job: '{job_id}'")

        # Run job logic
        outputValue = jobs.test_job()

        # Store output and complete status
        job_io.update_field(job_id, "output", outputValue)
        job_io.update_field(job_id, "status", "completed")
        print("job finished")
    else:
        print("no jobs in queue")
        time.sleep(10)
